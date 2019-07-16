"""
author @22PoojaGaur

This file takes tesco provided concept hierarchy dataset and cleans it.

Input format -

num.[item-name]
{PATH=}[Item-path-separated-by-/]

Output format -

[item-name]
[item-path-separated-by-spaces]
"""
import sys

def main():
	file_name = sys.argv[1]
	out_file_name = sys.argv[2]

	try:
		fin = open(file_name, 'r')
		fout = open(out_file_name, 'w')

	except:
		print "ERROR: Enter correct file name"
		sys.exit()


	is_item_line = 1
	line = ''

	for line in fin.readlines():
		if is_item_line:
			# modify and write item line
			it_name = line.split('.')[1].strip()
			fout.write(it_name.replace(' ', '_') + '\n')
			is_item_line = 0
		else:
			# modify and write path line
			full_path = line.split('=')[1]
			path_array = full_path.split('/')

			for category in path_array:
				fout.write(category.strip().replace(' ', '_') + ' ')
			fout.write('\n\n')

			is_item_line = 1

	fin.close()
	fout.close()


if __name__ == '__main__':
    main()
