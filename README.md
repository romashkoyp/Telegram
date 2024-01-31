# Description

## Data preparation

### Download and save JSON data from Telegram channels
Data in JSON format was downloaded from Telegram directly for 11 Telegram channels using Desktop Telegram interface and saved in separate directory. Each channel has own directory with own JSON file with posts. **Sum of posts for 11 JSON files is 49714**. Period of posts is from date of channels` creation to 30.01.2024.

### Data cleaning and formatting
Python script https://github.com/romashkoyp/Telegram/blob/master/02_many_json_to_one_json.py detects JSON files in folder and subfolders, extracts only text data from these JSON files and cleans text data from emojies, whitespaces and unusual characters, creates only one JSON file with all data from all JSON files.
Clean text method is:
```
if post_text:
    full_text = ''.join(item.get('text', '') if isinstance(item, dict) else item for item in post_text)
    lines = [line for line in full_text.splitlines() if line.strip()]
    cleaned_text = ' '.join(lines)

    # Define a list of allowed symbols
    allowed_symbols = ['«', '»', '.', ',', '!', '?', ':', ';', '(', ')', '[', ']', '{', '}', '&', '@', '#', '$', '%', '^', '*', '+', '-', '=', '_', '<', '>', '|', '/', '\\']

    # Remove emojis and unwanted symbols using regex
    cleaned_text = re.sub(r'[^\w\s{}]+'.format(''.join(re.escape(symbol) for symbol in allowed_symbols)), '', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
```

In output JSON file we get **19011 posts** with structure:
```
{
    "channel":
    "post_id":
    "global_post_id":
    "post_date":
    "post_text":
}
```
