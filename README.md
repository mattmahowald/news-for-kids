# News For Kids Parsing Script

Note: Documentation written based on CLI running bash.

## To run the script

1. Download python3
2. Install pip with the command `python3 get-pip.py` from the project directory.
3. Install the necessary packages with `python3 -m pip install -r requirements.txt`
4. Type into the prompt `which python3` and replace the first line of the news-4-kids.py file with `#!<your terminal's response`>
5. Run the script by executing the command `python3 news-4-kids.py`, which should prompt you to fire up a web-browser and authenticate. Do so using the newsforkids@lightsailed.com email.
6. Once authenticated, the script should create a folder in the Daily Emails folder in Google Drive. Check to assure the new folder with the correct date (folder name YYYYMMDD) was uploaded at the time you ran the script.
7. After verifying this works, schedule a job to run this command (NOTE: in order to use the email functionality, set the daily job to execute the command with the flag `c` or `--cron`, so the command will appear `python3 news-4-kids.py -c`.

Verify this works the next morning.

### Troubleshooting

There are a couple of known issues that can arise when running this script over a period of time:
- The headers fo the JSON data may change. If newsomatic renames their content, simply alter the `HEADERS` dictionary.
- The Google Drive folder key is specific to the newsforkids lightsail account. If it changes, alter the `PARENT_ID` key based on the instructions in the comment in the code.
- The newsomatic API URL may change, in which case replace the `URL` field with the new link. If this is the case, we should be contacted by newsomatic.