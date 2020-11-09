# TODO auto prepare all branches or manually changes branches ?

import os, shutil, subprocess

# UTILS

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def commit_changes(commit_msg):
    git1 = "git add ."
    git2 = "git commit -m \"%s\"" % commit_msg
    subprocess.call(git1.split(" "))
    # VFE TODO fix & test s.t. verbose messages are not splitted
    subprocess.call(git2.split(" "))

# 4) C/P doc dev rst content --> c/c or take from ../odoo/doc ??? (MAKE SURE VERSION IS CORRECT ONE)
# Create new doc structure
# Move files by script
# TODO add master branch (next 15.0 ?)

static_copy = "generic/"
doc_user = "documentation-user/"
doc_dev = "odoo/doc/"

def _static():
    # copy all files from doc_dev/_static/ to doc_user/_static
    pass

def _extensions():
    # 1) _extensions/odoo --> _extensions/odoo_ext
    os.rename("_extensions/odoo", "_extensions/odoo_ext")
    commit_changes("STEP1") # TODO update commit msg
    # 2) reset _extensions to new generic directory content
    # os.rmdir only works for empty dirs
    # delete existing content
    shutil.rmtree('_extensions/odoo_ext')
    # recreate directory
    os.mkdir('_extensions/odoo_ext')
    # copy content
    copytree(static_copy + "odoo_ext", '_extensions/odoo_ext')
    commit_changes("STEP2") # TODO update commit msg

def _config():
    # NOTE: not tested atm
    os.unlink('conf.py')
    shutil.copyfile(static_copy + "/conf.py", "conf.py")
    commit_changes("STEP3")
    # cp new joint config ? NOTE: Still has to be verified to keep as much args as possible.
    pass

def _rem_demo_link():
    # To call manually + grep .. demo:: in files and remove.
    pass

def _new_structure():
    # index.rst
    # applications - administration - developer - contributing - services
    # copy new structure from static_copy
    # Make sure the main rst files (index.rst + main sub rst)
    # are correctly specified
    pass

def _resolve_mapping():
    # TODO infer files to move from toctree ?
    for fro, to in MAPPING:
        # if fro endswith .rst:
        # move unique file
        # elif fro+.rst exists:
        # mv file + folder content
        # else:
        # only move directory content ?
        pass
    # Do we already specify the generic indexes in the new structure ?
    # If yes, mapping resolution will be easier (no need to modify main indexes)
    # only the files whose depths are modified.
    pass

def _applications_step():
    applications = _get_applications_files()
    for application in applications:
        # mv "application" folder to applications/
        # mv "application".rst to the application folder
        # format file to replace "application"/file by file
        # TODO support one file apps ?
        # ADD a list of specific case to manage ? e.g. mobile/firebase ?
        pass
    # mv applications.rst
    # format applications.rst to duplicate references
    # eg. accounting --> accounting/accounting
    return

def _get_applications_files():
    application_index = doc_user + "applications.rst"
    # open applications.rst
    # return all toctree items (pairs "folder/file")
    # NB do not forget to add the .rst when using them later ?
    # - db_management which should be considered specifically
    return []

def _format_application_file(file_path, txt_to_remove):
    # TODO pattern to fill with toctree content:
    # meta, page title, sub pages
    # file.open
    # file.replace(txt_to_remove, "") ?
    # file.close
    return

MAPPING = [
    # from, to, dir? # add format option ?
    # PRE Processing
    (doc_user + 'odoo_sh/documentation.rst', doc_user + "odoo_sh/odoo_sh.rst"),
    # 1) Applications: Specific method + settings page (or user_settings ?)
    (doc_user + 'db_management/documentation.rst', doc_user + 'applications/settings.rst'),
    # TODO settings page from db_management
    # TODO some medias from db_management/documentation.rst to move manually ?
    # make a git patch for that ?

    # 2) Administration
    # VFE FIXME what do we do with setup/update.rst ?
    (doc_dev + 'setup/install.rst', doc_user + "administration.rst"),
    (doc_dev + 'setup/deploy.rst', doc_user + "administration/deployment/deploy.rst"),
    (doc_dev + 'setup/cdn', doc_user + "administration/deployment/cdn"),
    (doc_dev + 'setup/email_gateway.rst', doc_user + "administration/deployment/email_gateway.rst"),
    # Specific case, the doc is odoo_sh/documentation
    # TODO pre-rename ?
    # upgrade.rst: static ref to upgrade.odoo.com or reuse update.rst ?
    (doc_user + 'odoo_sh', doc_user + "administration/odoo_sh"),
    (doc_dev + 'setup/enterprise', doc_user + "administration/enterprise"),
    (doc_user + 'db_management/db_online', doc_user + 'administration/d2d/db_online'),
    (doc_user + 'db_management/db_premise', doc_user + 'administration/d2d/db_premise'),

    # 3) Dev doc
    # VFE FIXME Webservices scope was forgotten, keep here ?
    (doc_dev + 'reference', doc_user + 'developer/reference'),
    # (doc_dev + 'tutorials', doc_user + 'developer/tutorials'), # only in 14 + ?
    (doc_dev + 'howtos', doc_user + 'developer/howtos'),
    (doc_dev + 'webservices', doc_user + 'developer/webservices'), # TODO move localization to howtos
    # TODO when using mapping, do not forget to append .rst to files from & to
    # For each mapping, move .rst file AND if exists move directory with same name ?
]

NEW_ORG = {
    "Applications": {
        # All apps
        # Settings (ex db_management/documentation) --> TODO STATIC
    },
    "Administration": { # TODO static ?
        # Install
        # Deployment
            # TODO title dev/setup/deploy
                # or merge the three pages together ?
            # Deployment with CDNs (dev/setup/cdn)
            # Email gateway (setup/email_gateway)
        # Upgrade # TODO static ref to upgrade.odoo.com # no file
        # Odoo.sh #
        # Day to day database management
            # Online (user/db_management/db_online)
            # On premise (user/db_management/db_premise)
        # From community to enterprise (dev/setup/enterprise)
    },
    "Developer": {
        # Reference
        # Webservices :
            # IAP
            # Upgrade
            # Odoo rpc
        # Tutorials ?
        # How-to's
    },
    "Services": { # TODO static
        # Support
        # Consultancy (success packs, ...)
        # Partners
        # Legal
    },
    "Contributing": { # TODO static
        # Documentation
        # Translation
        # Codebase
        # TODO move localization construction here ?
    },
}

def _auto_post_process():
    # TODO log (and/or remove) remaining files after restructuration
    #   business.rst file and mementoes ?
    # TODO move legal files to legal/media and update static refs ?
    # TODO demo_link removal (manual amend of commit to remove .. demo:: commands)
    # Update .CODEOWNERS file ?
    pass

# Dropped pages/features:
# Demo links
# business.rst file, the mementos are referenced from the inner pages of the doc anyway.

# TODO other files to make advanced rst and/or structure post-processing ?
# e.g. full depth reordering ?