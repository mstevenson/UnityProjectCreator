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
import configparser

config = configparser.ConfigParser()

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

if __name__ == '__main__':
	config_path = 'config.ini'
	if os.path.exists(config_path):
		config.read('config.ini')
	else:
		config['Settings'] = {
			'company' : 'Default Company',
			'unity_version' : '2017.4.17f1',
			#'timestep' : '0.0111111',
			#'enable_vr' : 'true'
		}
		with open(config_path, 'w') as configfile:
			config.write(configfile)

	product = raw_input('Enter a Unity project name: ')

	output_dir = "output"
	create_dir(output_dir)
	path = os.path.join(output_dir, product)

	if os.path.exists(path):
		print('Project already exists')
		quit()

	create_dir(path)

	company = config['Settings']['company']
	unity_version = config['Settings']['unity_version']

	# Create Unity project
	create_dir(os.path.join(path, 'Assets'))
	project_settings_dir = os.path.join(path, 'ProjectSettings')
	copy_template('ProjectSettings', project_settings_dir)
	copy_template('Main.unity', os.path.join(path, 'Assets', 'Main.unity'))
	for filename in os.listdir(project_settings_dir):
		filepath = os.path.join(project_settings_dir, filename)
		with open(filepath, 'r') as f:
			text = f.read()
			text = text.replace(r'##DefaultCompany##', company)
			text = text.replace(r'##DefaultProduct##', product)
			text = text.replace(r'##UnityVersion##', unity_version)
		with open(filepath, "w") as f:
			f.write(text)

	# Create IDE files
	copy_template('editorconfig', os.path.join(path, '.editorconfig'))
	copy_template('Project.sln', os.path.join(path, product + ".sln"))
	
	# Initialize Git
	copy_template('gitignore', os.path.join(path, '.gitignore'))
	copy_template('gitattributes', os.path.join(path, '.gitattributes'))
	
	print('Created project ' + path)

