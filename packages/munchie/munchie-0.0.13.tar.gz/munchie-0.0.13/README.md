# Munchie

Munchie is a simple file object manager to manipulate and store directories and files.  

---

## Compatibility
* Munchie works with Linux, OSX, and Windows.  
* Requires Python 3.7 or later.  

---

## Installing
Install with `pip3` or your favorite PyPi package manager.  
```
pip install munchie
```

---

## Using FileMuncher

To begin better controlling your files and directories it is as easy as importing and constructing a FileMuncher object.  
```
from munchie.file_muncher import FileMuncher

file_muncher = FileMuncher()
```

### Default attributes

By default FileMuncher loads the current working directory as well as the user home directory into respective attributes.  
The attributes can be accessed by calling them from the constructed FileMuncher object.  
```
file_muncher.base_dir  # current working directory
file_muncher.home_dir  # user home directory
```

### Create a new directory

To create a new empty directory simply call the function and provide the path.  
```
# create 'new_directory' in the user home folder
file_muncher.create_new_directory(f'{file_muncher.home_dir}/new_directory')
```

### Create a new file

To create a new empty file simply call the function and provide the path.  
```
# create 'new_file.test' in the user home folder
file_muncher.create_new_file(f'{file_muncher.home_dir}/new_file.test')
```

### Read file

FileMuncher is able to read in various file types and return the contents in a format that can be manipulated.  
Supported extensions include:

<table>
<thead>
  <tr>
    <th>Type</th>
    <th>Extensions</th>
    <th>Return Type</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>csv</td>
    <td>.csv</td>
    <td>list of dicts</td>
  </tr>
  <tr>
    <td>config</td>
    <td>.cfg, .conf, .ini</td>
    <td>dict</td>
  </tr>
  <tr>
    <td>json</td>
    <td>.json</td>
    <td>dict</td>
  </tr>
  <tr>
    <td>text</td>
    <td>.nfo, .text, .txt</td>
    <td>list</td>
  </tr>
  <tr>
    <td>yaml</td>
    <td>.yaml, .yml</td>
    <td>dict</td>
  </tr>
</tbody>
</table>

To read in the contents of a file all you need is the path to the file. FileMuncher will determine the file extension and how to open the file for you.  
```
# read in 'new_file.json' and return the contents as dict
contents = file_muncher.read_file(f'{file_muncher.home_dir}/new_file.json')
```

### Remove a directory

FileMuncher can also be used to cleanup directories. Provide the path the directory you wish to remove and all of the contents as well as the directory itself will be removed.  
```
# prompt to remove directory 'new_dir'
file_muncher.remove_directory(f'{file_muncher.home_dir}/new_dir')
```
By default this command will require confirmation input from the user to verify prior to deletion. The confirmation requirement can be toggled off by setting the `force` flag.  
```
# remove directory 'new_dir' without confirmation check
file_muncher.remove_directory(f'{file_muncher.home_dir}/new_dir', force=True)
```

### Remove a file

In addition to directories FileMuncher can also remove files by providing the path the file you wish to remove
```
# prompt to remove file 'new_file.test'
file_muncher.remove_file(f'{file_muncher.home_dir}/new_file.test')
```
By default this command will require confirmation input from the user to verify prior to deletion. The confirmation requirement can be toggled off by setting the force flag.  
```
# remove file 'new_file.test' without confirmation check
file_muncher.remove_file(f'{file_muncher.home_dir}/new_file.test', force=True)
```

### Rotate files

FileMuncher is capable of rotating old or stale files based on the their last modified date.
```
# prompt to rotate files in directory 'old_logs'
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs')
```

You can specify how many days old files to rotate should be by setting the `days_old` parameter. Default is 14.
```
# prompt to remove files in directory 'old_logs' older than 30 days
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs', days_old=30)
```

In the same way removing directories and individual files works rotating also prompts for confirmation. This too can be toggled off with a `force` flag.  
```
# remove files in directory 'old_logs' older than 30 days without confirmation check
file_muncher.rotate_files(f'{file_muncher.home_dir}/old_logs', days_old=30, force=True)
```


### Update Path

New directory and file paths can be added to the FileMuncher object. Existing paths can also be updated.  
Whether creating a new path or updating an existing the only requirements are the `attribute_name` and the `attribute_path`
```
# create a new attribute called 'new_file' that points to 'new_file.test' located in the user home directory
file_muncher.update_path(attribute_name='new_file', attribute_path=f'{file_muncher.home_dir}/new_file.test')

# update an existing path to point somewhere new
file_muncher.update_path(attribute_name='base_dir', attribute_path='/Users/username/Documents/testing')
```
When creating or updating a path you have the option to create a blank directory or empty file at the same time by specifying the `is_dir` or `is_file` flags. Only one flag may be chosen as a path cannot be both a directory and a file.
```
# create a new directory attribute and create the directory on the filesystem
file_muncher.update_path(attribute_name='new_dir', attribute_path=f'{file_muncher.home_dir}/new_dir', is_dir=True)

# create a new file attribute and create the file on the filesystem
file_muncher.update_path(attribute_name='new_file', attribute_path=f'{file_muncher.home_dir}/new_file.test', is_file=True)
```

### Write file

Update or create a new file with contents. Supports the following file types:
* .csv
* .cfg, .conf, .ini
* .json
* .nfo, .text, .txt
* .yaml, .yml

To write contents to a file simply pass the contents you want to write and the path to save the contents to.  
```
# prepare dict contents
contents = {
    "file": "muncher"
}
# write the contents to a json file
file_muncher.write_file(contents, f'{file_muncher.home_dir}/new_file.json')
```
