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
import configparser

template_dir = 'templates'
config = configparser.ConfigParser()

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def copy_template(source, dest):
	s = os.path.join(template_dir, source)
	if (os.path.isfile(s)):
		shutil.copy2(s, dest)
	else:
		shutil.copytree(s, dest)

def initialize_git(path):
	copy_template('gitignore', os.path.join(path, '.gitignore'))
	copy_template('gitattributes', os.path.join(path, '.gitattributes'))

def create_unity_project(path, company, product, unity_version):
	path = os.path.expanduser(path)
	if os.path.exists(path):
		return False
	create_dir(os.path.join(path, 'Assets'))
	project_settings_dir = os.path.join(path, 'ProjectSettings')
	copy_template('ProjectSettings', project_settings_dir)
	for filename in os.listdir(project_settings_dir):
		filepath = os.path.join(project_settings_dir, filename)
		with open(filepath, 'r') as f:
			text = f.read()
			text = text.replace(r'%%DefaultCompany%%', company)
			text = text.replace(r'%%DefaultProduct%%', product)
			text = text.replace(r'%%UnityVersion%%', unity_version)
		with open(filepath, "w") as f:
			f.write(text)
	return True

def create_ide_files(path):
	copy_template('editorconfig', os.path.join(path, '.editorconfig'))

if __name__ == '__main__':
	config_path = 'config.ini'
	if os.path.exists(config_path):
		config.read('config.ini')
	else:
		config['Settings'] = {
			'company' : 'Default Company',
			'product' : 'Default Product',
			'unity_version' : '2017.4.17f1',
			#'timestep' : '0.0111111',
			#'enable_vr' : 'true'
		}
		with open(config_path, 'w') as configfile:
			config.write(configfile)

	path = raw_input('Enter a new Unity project folder path: ')
	success = create_unity_project(path, config['Settings']['company'], config['Settings']['product'], config['Settings']['unity_version'])
	if not success:
		print('Project already exists')
		quit()
	create_ide_files(path)
	initialize_git(path)
	print('Created project ' + path)

