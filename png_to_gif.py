import os
import imageio
import glob
import sys

def main(path,fname):
  # Create the frames
  frames = []
  imgs = sorted(glob.glob( path + '/' + '*.png'))
  for i in imgs:
      frames.append(imageio.imread(i))

  # Save into a GIF file that loops forever
  imageio.mimsave(fname + '.gif', frames,
                  fps = 5)


if __name__ == '__main__':
  main(sys.argv[1],sys.argv[2])