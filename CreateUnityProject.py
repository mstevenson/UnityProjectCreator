#!/usr/bin/env python

# TODO
# x Create Unity project structure.
# x Set Unity to .Net 4.5 mode.
# x Enable XR settings, and set up "None" and "Oculus".
# x Add .gitignore and .gitattributes.
# x Add .editorconfig
# x Add .sln file with some preconfigured settings
# x Set the company and product name in Unity meta files
# x Enforce Unix line endings in Unity and IDE
# - Add Rider prefs file for the specific .sln
# - Initialize git
# - Initialize git-lfs.
# - Import Oculus Integration from the Asset Store, or as a submodule.
# - Replace Unity project GUID and main scene GUID

import os
import os.path
import shutil
import uuid
import argparse
from git import Repo

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def copy_template(source, dest):
	template_dir = 'templates'
	s = os.path.join(template_dir, source)
	if (os.path.isfile(s)):
		shutil.copy2(s, dest)
	else:
		shutil.copytree(s, dest)

def create_guid():
	guid = uuid.uuid4()
	return str(guid).replace('-', '')

def replace_template_tags(path):
	# replacements to add:
	#    - timestep
	#    - enable_vr
	with open(path, 'r') as f:
		text = f.read()
		text = text.replace(r'##DefaultCompany##', args.company)
		text = text.replace(r'##DefaultProduct##', args.product)
		text = text.replace(r'##SceneGuid##', scene_guid)
		text = text.replace(r'##ProjectGuid##', project_guid)
		# text = text.replace(r'##UnityVersion##', unity_version)
	with open(path, "w") as f:
		f.write(text)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Create an empty Unity project.')
	parser.add_argument('--company', default='Default Company', type=str)
	parser.add_argument('product', help='the name of the Unity project')
	args = parser.parse_args()

	output_dir = "output"
	create_dir(output_dir)
	project_path = os.path.join(output_dir, args.product)

	if os.path.exists(project_path):
		print('Project already exists: ' + project_path)
		quit()

	create_dir(project_path)

	# Create Unity project
	create_dir(os.path.join(project_path, 'Assets'))
	project_settings_dir = os.path.join(project_path, 'ProjectSettings')
	copy_template('ProjectSettings', project_settings_dir)

	project_guid = create_guid()
	scene_guid = create_guid()

	for filename in os.listdir(project_settings_dir):
		filepath = os.path.join(project_settings_dir, filename)
		replace_template_tags(filepath)

	# TODO replace the id in Main.unity.meta with scene_guid var
	copy_template('Main.unity', os.path.join(project_path, 'Assets', 'Main.unity'))
	meta_path = os.path.join(project_path, 'Assets', 'Main.unity.meta')
	copy_template('Main.unity.meta', meta_path)
	replace_template_tags(meta_path)

	# Create IDE files
	copy_template('editorconfig', os.path.join(project_path, '.editorconfig'))
	copy_template('Project.sln', os.path.join(project_path, args.product + ".sln"))
	
	# Initialize Git project
	copy_template('gitignore', os.path.join(project_path, '.gitignore'))
	copy_template('gitattributes', os.path.join(project_path, '.gitattributes'))

	repo = Repo.init(project_path)
	#repo.create_submodule
	repo.index.add('*')
	repo.commit('Created Unity project ' + args.product)
	
	print('Created Unity project: ' + project_path)

