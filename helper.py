import sys
import os


from pathlib import Path


FIRST_PARAM = 1
programming_file_suffixes = {
    '.py',
    '.java',
    '.c',
    '.cpp',
    '.cs',
    '.ts',
    '.js',
}


def create_git_ignore(suffix_file_names, suffix, directory_path):
    with open(directory_path + '.gitignore', 'w') as gitignore:
        for key in suffix_file_names:
            if key != suffix:
                gitignore.write(f'*{key}\n')


def delete_unnecessary_files(suffix_file_names):
    delete_count = 0
    for key in suffix_file_names:
        for file_name in suffix_file_names[key]:
            os.remove(file_name)
            delete_count += 1
    return delete_count


def remove_last_modified_file(suffix_file_names, most_popular_suffixes):
    file_name = ''
    max_modified_time = 0
    file_names = []
    for suffix in most_popular_suffixes:
        file_names += suffix_file_names[suffix]
    for file in file_names:
        modified_time = os.path.getmtime(file)
        if modified_time > max_modified_time:
            max_modified_time = modified_time
            file_name = file

    suffix = Path(file_name).suffix
    suffix_file_names[suffix].remove(file_name)

    return suffix


def get_most_popular_extensions(suffix_file_names):
    suffix = ''
    max_count = 0
    most_popular_suffixes = []
    for key in suffix_file_names:
        if key in programming_file_suffixes:
            suffix_count = len(suffix_file_names[key])
            if suffix_count == max_count:
                most_popular_suffixes.append(key)
            elif suffix_count > max_count:
                most_popular_suffixes = [key]
                max_count = suffix_count

    return most_popular_suffixes


def get_top_level_file_names_and_suffixes_in_dir(directory):
    suffix_file_names = {}
    listdir = os.listdir(directory)
    for el in listdir:
        if os.path.isfile(directory + el):
            suffix = Path(el).suffix
            suffix_file_names.setdefault(suffix, [])
            suffix_file_names[suffix].append(directory + el)

    # return dictionary with key as suffix and value as file names with this extension.
    return suffix_file_names


def is_input_correct(argc, argv):
    if argc == 1:
        print('You must specify the path to the directory.')
        return False

    directory_path = argv[FIRST_PARAM]
    if not os.path.isdir(directory_path):
        print(f'{directory_path} is not a correct path to the directory.')
        return False

    return True


def add_back_slash(directory_path):
    if directory_path[-1] != '\\':
        directory_path += '\\'
    return directory_path


def main(params):
    if not is_input_correct(len(params), params):
        return 1

    directory_path = add_back_slash(params[FIRST_PARAM])
    suffix_file_names = get_top_level_file_names_and_suffixes_in_dir(directory_path)
    most_popular_suffixes = get_most_popular_extensions(suffix_file_names)
    suffix = remove_last_modified_file(suffix_file_names, most_popular_suffixes)
    delete_count = delete_unnecessary_files(suffix_file_names)
    create_git_ignore(suffix_file_names, suffix, directory_path)

    print(f'You just helped {suffix} developer find the latest version of his code! .gitignore is created. '
          f'{delete_count} files deleted.')

    return 0


if __name__ == '__main__':
    input_params = sys.argv
    main(input_params)
