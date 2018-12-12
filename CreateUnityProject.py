#!/usr/bin/env python

# TODO
# x Create Unity project structure.
# x Set Unity to .Net 4.5 mode.
# x Enable XR settings, and set up "None" and "Oculus".
# x Add .gitignore and .gitattributes.
# - Add .editorconfig
# - Add .sln file with some preconfigured settings
# - Add Rider prefs file for the specific .sln
# - Initialize git
# - Initialize git-lfs.
# - Clone LighthausFrameworks as a submodule.
# - Import Oculus Integration from the Asset Store, or as a submodule.
# - Set the company and product name in Unity meta files
# - Enforce Unix line endings in Unity and IDE

import os
import os.path
import shutil

template_dir = "templates"

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def copy_template(source, dest):
	shutil.copy2(os.path.join(template_dir, source), dest)

def initialize_git(path):
	copy_template("gitignore_template", os.path.join(path, ".gitignore"))
	copy_template("gitattributes_template", os.path.join(path, ".gitattributes"))

def create_unity_project(path):
	path = os.path.expanduser(path)
	if os.path.exists(path):
		return False
	create_dir(os.path.join(path, "Assets"))
	create_dir(os.path.join(path, "ProjectSettings"))
	return True

if __name__ == "__main__":
	path = raw_input("Enter a new Unity project folder path: ")
	success = create_unity_project(path)
	if not success:
		print('Project already exists')
		quit()
	initialize_git(path)
	print('Created project ' + path)

