---
name: claude-video-direction
description: Make motion-graphics videos and video edits with Claude using only code (HTML, CSS, JavaScript, Three.js, ffmpeg) - no generative video model - and get them to production quality in three levels - one-shot showreel prompts, storyboarding before rendering, and directing the rendered video with timestamped, pinned comments on frames and audio. Use when someone wants Claude to make or edit a video, an animated explainer, a showreel, animated SVG icons, or asks how to give Claude feedback on video.
---

# Video and motion graphics with Claude

## How it works

Claude makes the whole video in code: images and graphics from the workspace placed at exact positions and timestamps with
JavaScript, motion in HTML/CSS/JS, 3D with Three.js, then rendered and muxed with ffmpeg. No generative video model.
Libraries like Hyperframes or Remotion are optional - current models do it natively.
Ask for graphics as **SVG**: they scale without blur, you can edit colours by hand, and Claude can animate them.

## Level 1 - one-shot

*"Make a dynamic motion-graphics video that showcases what you can do. Push 3D elements."*
Good for: testing a new model (keep a ceiling-pushing prompt and re-run it on every release) and quick showreels for a
portfolio. It rarely reaches production quality: a vague prompt lets the model spend all its tokens rendering the wrong video.

## Level 2 - storyboard first

Ask for a storyboard before any animation: the scenes built as HTML but **static screenshots per scene + a description of
the motion** ("camera whips to panel 1, continues across the panels..."). Cheap and fast to review, so you steer before the
expensive render.

Feedback works best **on the frame**, not in chat: a review page where you click a frame, pin a comment, and the comment
carries the timestamp and the x/y point. Go through the whole storyboard, copy all comments, paste them to Claude, then ask
for a new storyboard or go straight to video.

## Level 3 - direct the rendered video

Storyboard feedback gets you ~80-90 % there. Directing is reviewing the actual render:

- a review editor that plays the video (2x speed is fine), lets you pin comments on frames **and on the audio/sound
  effects** (not reviewable at storyboard stage), each with timestamp and position ("remove this scene", "focus on the page
  title - here is the link");
- copy all comments for all clips, send to Claude, let it update, re-review, then render the final;
- for talking-head footage, first have Claude pick the takes to keep, then animate on top.

As models improve you need fewer comments. Your taste and your feedback system are the differentiators.

## Rules for Claude

- Default to storyboard first unless the user asks for a one-shot.
- Every comment you receive has a timestamp and position - change exactly that, report what changed per comment.
- Offer a "teach the skill" option: fold recurring feedback into the cut/animate skills (see `os-skills-routines`).
- Keep a style reference (brand design system) and produce some wildcard styles on request.
