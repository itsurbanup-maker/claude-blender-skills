# Blender via MCP

Instead of running `bridge.py` by hand, Claude can control Blender through the
[`blender-mcp`](https://github.com/ahujasid/blender-mcp) server. Claude then gets tools such as
`get_scene_info`, `get_object_info`, `execute_blender_code` and `get_viewport_screenshot`.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) (it provides `uvx`).
2. Download `addon.py` from the blender-mcp repository. In Blender: **Edit > Preferences > Add-ons > Install**, pick `addon.py`, enable it.
3. In the 3D viewport press **N**, open the **BlenderMCP** tab, click **Connect to Claude**. Blender now listens on `127.0.0.1:9876`.
4. Claude Code picks up `.mcp.json` from this repo (or from the plugin) automatically. Run `/mcp` and check that `blender` is connected.

Manual alternative: `claude mcp add blender -- uvx blender-mcp`.

## Important

- `bridge.py` and the MCP add-on both use port **9876**. Run only one of them at a time.
- The skills' scripts are plain Blender Python. With MCP, Claude sends them through `execute_blender_code` instead of `send.py`.
- `execute_blender_code` runs arbitrary Python inside Blender. Only connect to Claude sessions you trust, and save your .blend first.
- Long renders should still be started from the command line (see the README), not through MCP, because the MCP call blocks Blender.
