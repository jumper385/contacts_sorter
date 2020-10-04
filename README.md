# Contacts Sorter CLI 💻
## Objective 🤘
Create a contacts sorter in CLI form that can merge two preformatted csv files of the form below. This should return a merged csv file.
| firstname | lastname   | mobile       | email1                   | email2                      |
|-----------|------------|--------------|--------------------------|-----------------------------|
| kai       | Danilovich | 599-460-9206 | kdanilovich0@example.com | kdanilovich0@soundcloud.com |
|           | Vinsen     |              | jvinsen2@bloglines.com   |                             |
| Gaby      | Yockley    |              |                          | gyockley6@photobucket.com   |
| ...       | ...        | ...          | ...                      | ...                         |

## What You'll Need 🧙‍♂️
- [ ] Two formatted CSV's with Contacts
- [ ] Terminal
- [ ] Free Computer Space
- [ ] (Optional) Configuration File

## Instructions 📚
### Config File ✨
1. Add the two contacts csv files to the root folder
2. Create a configuration file `conf.txt`
3. Inside the file, apply your configurations formatted as per: `filename1:your_first_list.csv|filename2:your_second_list.csv|outname:our_desired_filename.csv` and save your changes
4. In the project's root folder, type `python main.py --conf=conf.txt` in terminal
5. Open the new file and enjoy!
### Manual File Entry 👌
1. Add the two contacts csv files to the root folder
2. In the project's root folder, type `python main.py --f1=your_first_list.csv --f2=your_second_list.csv --out=your_desired_filename.csv` in terminal
3. Open the new file and enjoy!