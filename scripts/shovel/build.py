from os.path import join
from shovel import task
import os
import imp
import shutil
import subprocess

file = os.path.normpath(os.path.join(os.path.dirname(__file__), 'config.py'))
config = imp.load_source('config', file)


@task
def js():#(nomin=False): #TODO: add minification
  """Compiles javascript using closure"""

  try:
    shutil.rmtree(config.JS_DEST, ignore_errors=True)
    os.makedirs(config.JS_DEST)
  except:
    pass

  js_files = []
  for dirpath,dirnames,filenames in os.walk(join(config.JS_PATH, 'hutmap')):
    for filename in filenames:
      path = join(dirpath, filename)
      if filename.endswith('js'):
        if filename.startswith('app') or filename.startswith('module'):
          js_files.insert(0, path)
        else:
          js_files.append(path)

  cmd = ['java', '-jar', config.CLOSURE_COMPILER]
  cmd.append('--js')
  cmd.extend(' --js '.join(js_files).split(' '))
  cmd.extend(['--compilation_level', 'WHITESPACE_ONLY'])
  cmd.extend(['--js_output_file', '{0}/hutmap.min.js'.format(config.JS_DEST)])

  subprocess.check_call(cmd)

  set_permissions(config.JS_DEST)


@task
def css(nomin=False):
  """Compiles less files into public/static/css/hutmap.min.css"""
  try:
    shutil.rmtree(config.CSS_DEST, ignore_errors=True)
    os.makedirs(config.CSS_DEST)
  except:
    pass

  cmd = ['lessc']
  if str(nomin).lower() == 'false': cmd.append('--yui-compress')
  cmd.append(join(config.CSS_PATH, 'hutmap.less'))
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  stdoutdata,stderrdata = proc.communicate()
  if proc.returncode != 0:
    raise subprocess.CalledProcessError(proc.returncode, cmd)

  with open(join(config.CSS_DEST, 'hutmap.min.css'), 'w+') as file:
    file.writelines(stdoutdata)

  set_permissions(config.CSS_DEST)


def set_permissions(folder):
  """Sets permissions in public folder so Apache will serve files."""
  for dirpath,dirnames,filenames in os.walk(folder):
    os.chmod(dirpath, 0755)
    for filename in filenames:
      path = join(dirpath, filename)
      os.chmod(path, 0755)


