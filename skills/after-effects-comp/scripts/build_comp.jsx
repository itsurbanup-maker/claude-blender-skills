// After Effects (ExtendScript). Builds the film from a rendered PNG sequence:
//   one comp per shot, a FILM comp with the shots in order, the sound mix, one marker per shot,
//   a LOOK adjustment layer (lens, glow, grain; each one optional), an optional title, and a render queue item.
// Run with run_jsx.py, which writes config.jsxinc next to this file from your shots.json.
// Needs: Edit > Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" (for the log).
#include "config.jsxinc"

(function () {
    var log = [];
    function say(s) { log.push(s); $.writeln(s); }
    function pad(n, w) { var s = String(n); while (s.length < w) s = "0" + s; return s; }
    function frameFile(pattern, n) { // "C:/x/f_%04d.png" + 12 -> C:/x/f_0012.png
        return pattern.replace(/%0(\d)d/, function (m, w) { return pad(n, parseInt(w, 10)); });
    }
    function setProp(fx, names, value) { // effect property names differ by AE language: try each, report misses
        for (var i = 0; i < names.length; i++) {
            try { fx.property(names[i]).setValue(value); return; } catch (e) {}
        }
        say("  could not set " + names[0] + " on " + fx.name);
    }
    function addFx(layer, matchName, label) {
        try { return layer.property("ADBE Effect Parade").addProperty(matchName); }
        catch (e) { say("  effect " + label + " (" + matchName + ") not available, skipped"); return null; }
    }
    function findItem(name) {
        for (var i = 1; i <= app.project.numItems; i++) if (app.project.item(i).name === name) return app.project.item(i);
        return null;
    }

    var C = CFG, fps = C.fps, ae = C.after_effects || {};
    app.beginUndoGroup("build film comp");
    try {
        if (findItem("FILM")) { say("FILM comp already exists in this project. Nothing changed. Delete it or open a new project."); return; }

        // 1. footage: the whole PNG sequence once
        var first = C.shots[0].first;
        var io = new ImportOptions(new File(frameFile(C.frames, first)));
        io.sequence = true;
        var seq = app.project.importFile(io);
        seq.mainSource.conformFrameRate = fps;
        seq.name = C.name + "_frames";
        var W = seq.width, H = seq.height;
        say("frames: " + seq.name + " " + W + "x" + H + " @ " + fps + " fps, starts at frame " + first);

        // 2. one comp per shot, the sequence offset so the shot's first frame is at 0
        var folder = app.project.items.addFolder("shots");
        var total = 0, shotComps = [];
        for (var i = 0; i < C.shots.length; i++) {
            var s = C.shots[i], n = s.last - s.first + 1;
            var c = app.project.items.addComp(s.name, W, H, 1.0, n / fps, fps);
            c.parentFolder = folder;
            var L = c.layers.add(seq);
            L.startTime = -(s.first - first) / fps;
            shotComps.push({ comp: c, start: total, name: s.name });
            total += n;
        }

        // 3. FILM comp: shots in order, markers, sound
        var film = app.project.items.addComp("FILM", W, H, 1.0, total / fps, fps);
        for (var j = shotComps.length - 1; j >= 0; j--) { // add last first so shot 1 ends up on top
            var sl = film.layers.add(shotComps[j].comp);
            sl.startTime = shotComps[j].start / fps;
            film.markerProperty.setValueAtTime(shotComps[j].start / fps, new MarkerValue(shotComps[j].name));
        }
        if (C.audio) {
            var aud = app.project.importFile(new ImportOptions(new File(C.audio)));
            var al = film.layers.add(aud);
            al.moveToEnd();
            say("sound: " + aud.name);
        }

        // 4. LOOK adjustment layer. Subtle by default: the look comes from the Blender lighting.
        var look = ae.look || {};
        var adj = film.layers.addSolid([1, 1, 1], "LOOK", W, H, 1.0, total / fps);
        adj.adjustmentLayer = true;
        if (look.lens_distortion) { // slight barrel distortion, like a real lens
            var lens = addFx(adj, "ADBE Optics Compensation", "Optics Compensation");
            if (lens) setProp(lens, ["Field Of View (FOV)", "Field of View (FOV)"], look.lens_distortion);
        }
        if (look.glow) {
            var glow = addFx(adj, "ADBE Glo2", "Glow");
            if (glow) {
                setProp(glow, ["Glow Threshold"], look.glow.threshold || 85);
                setProp(glow, ["Glow Radius"], look.glow.radius || 40);
                setProp(glow, ["Glow Intensity"], look.glow.intensity || 0.3);
            }
        }
        if (look.grain) addFx(adj, "VISINF Grain Implant", "Add Grain");
        if (!look.lens_distortion && !look.glow && !look.grain) adj.enabled = false;

        // 5. optional title
        if (ae.title) {
            var t = film.layers.addText(ae.title.text);
            t.inPoint = ae.title.start || 0;
            t.outPoint = (ae.title.start || 0) + (ae.title.duration || 3);
        }

        // 6. render queue: PNG sequence, so a crash loses one frame at most
        if (ae.frames_out) {
            var rq = app.project.renderQueue.items.add(film);
            var om = rq.outputModule(1);
            if (ae.om_template) {
                try { om.applyTemplate(ae.om_template); } catch (e) { say("output template '" + ae.om_template + "' not found, using the default"); }
            }
            om.file = new File(ae.frames_out);
            say("render queue: FILM -> " + ae.frames_out);
        }

        film.openInViewer();
        if (ae.project) { app.project.save(new File(ae.project)); say("saved " + ae.project); }
        say("FILM: " + C.shots.length + " shots, " + total + " frames (" + (total / fps).toFixed(2) + " s)");
    } catch (err) {
        say("ERROR line " + err.line + ": " + err.toString());
    } finally {
        app.endUndoGroup();
        if (ae.log) {
            try { var f = new File(ae.log); f.encoding = "UTF-8"; f.open("w"); f.write(log.join("\n")); f.close(); } catch (e) {}
        }
    }
})();
