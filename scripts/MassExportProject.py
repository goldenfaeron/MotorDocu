"""
Fusion 360 — Mass Export Project
=================================
Recursively walks a Data Panel project (all nested subfolders) and exports
every Fusion design (.f3d) it finds to STEP and 3MF, mirroring the project's
folder structure under a local output directory.

Install & run:
  1. In Fusion 360: Utilities tab -> Scripts and Add-ins (or Shift+S).
  2. Scripts tab -> green "+" -> Create -> name it (e.g. MassExportProject),
     Python, then click "Edit" and paste this whole file over the template.
  3. Set PROJECT_NAME below to match your Fusion project's exact name.
  4. Run it (select the script -> Run). You'll be asked to pick an output
     folder; it defaults to ~/Fusion_Export if you cancel.

Notes:
  - Opens each design read-only and closes it without saving (doc.close(False))
    — this will NOT modify anything in your Fusion project.
  - Only files with extension f3d/f3z are treated as designs; drawings (.dwg),
    PDFs, etc. are skipped.
  - Mesh refinement for 3MF is set to High.
  - This can take a while for a large project — a progress dialog shows status
    and lets you cancel.
"""

import os
import adsk.core
import adsk.fusion
import traceback

# =============================================================================
# CONFIGURE
# =============================================================================
PROJECT_NAME = 'StuR'          # must match the Fusion Data Panel project name exactly
EXPORT_STEP = True
EXPORT_3MF = True
DESIGN_EXTENSIONS = ('f3d', 'f3z')

# =============================================================================


def sanitize(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip() or 'unnamed'


def collect_files(folder, rel_path, out_list):
    """Recursively collect (dataFile, rel_path) pairs for every design file."""
    for f in folder.dataFiles:
        if f.fileExtension in DESIGN_EXTENSIONS:
            out_list.append((f, rel_path))
    for sub in folder.dataFolders:
        collect_files(sub, os.path.join(rel_path, sanitize(sub.name)), out_list)


def export_one(app, data_file, out_dir):
    """Open one data file, export it, close without saving. Returns (ok, error)."""
    doc = None
    try:
        doc = app.documents.open(data_file, False)
        if doc is None:
            return False, "documents.open returned None"

        design = adsk.fusion.Design.cast(app.activeProduct)
        if design is None:
            return False, "Active product is not a Fusion Design"

        export_mgr = design.exportManager
        base_name = sanitize(data_file.name)
        os.makedirs(out_dir, exist_ok=True)

        if EXPORT_STEP:
            step_path = os.path.join(out_dir, base_name + '.step')
            step_opts = export_mgr.createSTEPExportOptions(step_path)
            export_mgr.execute(step_opts)

        if EXPORT_3MF:
            mf_path = os.path.join(out_dir, base_name + '.3mf')
            mf_opts = export_mgr.createC3MFExportOptions(design.rootComponent, mf_path)
            mf_opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            export_mgr.execute(mf_opts)

        return True, None
    except Exception:
        return False, traceback.format_exc()
    finally:
        if doc is not None:
            try:
                doc.close(False)
            except Exception:
                pass


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # --- find the project ---
        hub = app.data.activeHub
        project = None
        for p in hub.dataProjects:
            if p.name == PROJECT_NAME:
                project = p
                break
        if project is None:
            names = ", ".join(p.name for p in hub.dataProjects)
            ui.messageBox(
                f"Project '{PROJECT_NAME}' not found in the active hub.\n\n"
                f"Available projects: {names}"
            )
            return

        # --- pick output folder ---
        default_output = os.path.join(os.path.expanduser('~'), 'Fusion_Export')
        folder_dlg = ui.createFolderDialog()
        folder_dlg.title = 'Select Output Folder for Mass Export'
        if folder_dlg.showDialog() == adsk.core.DialogResults.DialogOK:
            output_root = folder_dlg.folder
        else:
            output_root = default_output

        # --- collect every design file in the project tree ---
        all_files = []
        collect_files(project.rootFolder, sanitize(project.name), all_files)

        if not all_files:
            ui.messageBox(f"No design files (.f3d/.f3z) found in project '{PROJECT_NAME}'.")
            return

        # --- export with a progress dialog ---
        progress = ui.createProgressDialog()
        progress.cancelButtonText = 'Cancel'
        progress.isBackgroundTranslucent = False
        progress.show('Mass Export', 'Exporting %v of %m: %p%%', 0, len(all_files))

        exported, failed = [], []
        for i, (data_file, rel_path) in enumerate(all_files):
            if progress.wasCancelled:
                break
            progress.message = f'Exporting %v of %m: {data_file.name}'
            progress.progressValue = i
            out_dir = os.path.join(output_root, rel_path)
            ok, err = export_one(app, data_file, out_dir)
            if ok:
                exported.append(data_file.name)
            else:
                failed.append((data_file.name, err))

        progress.hide()

        msg = f"Exported {len(exported)} of {len(all_files)} design(s) to:\n{output_root}\n"
        if failed:
            msg += f"\nFailed ({len(failed)}):\n" + "\n".join(f"- {n}: {e.splitlines()[-1]}" for n, e in failed)
        ui.messageBox(msg)

    except Exception:
        if ui:
            ui.messageBox('Script failed:\n{}'.format(traceback.format_exc()))
