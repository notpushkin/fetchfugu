import yaml
from subprocess import check_call

config = yaml.load(open("config.yml"))['epub']

strip = lambda s: s.strip()

if __name__ == '__main__':
  options = ['pandoc']
  options += config['options']

  with open(config['index_file']) as index:
    for file in map(strip, index.readlines()):
      options.append(file)

  options += ['--epub-metadata', config['meta_file']]
  options += ['-o', config['output']]

  try:
    check_call(options)
  except:
    pass