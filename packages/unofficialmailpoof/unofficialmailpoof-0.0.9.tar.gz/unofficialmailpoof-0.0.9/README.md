# Installation

## Windows
Install Chrome and Chromedriver<br>
<code>choco install chromedriver</code><br>
Or if you need a specific version of chromedriver
<code>choco install chromedriver --version 89.0.4389.230</code>

## Debian/Ubuntu
<code>sudo apt install chromium-browser chromium-chromedriver</code>

## macOS
Install Chrome and Chromedriver<br>
<code>brew install chromedriver</code>

# Usage
Calling the module might take a minimum of 10 seconds
### Install module
<code>pip install unofficialmailpoof</code>

### Import it
<code>import unofficialmailpoof as mp</code>

### Use it
<code>print(mp.getallmails('john.doe@mailpoof.com'))<br>
print(mp.getallmails('john.doe'))</code><br>
If you want to see what the bot is doing, add argument 1 or True to getallmails like this:<br>
<code>print(mp.getallmails('john.doe@mailpoof.com',1))<code><br>
<code>print(mp.getallmails('john.doe@mailpoof.com',True))<code>

# Result
The output should look like this
<br>
['subject','sender@email.com','New York date and time','message',['links within the message']]
<br>
<br>
[['First Mail!', 'emailsender1@email.com', '15 Apr 2021 02:40 AM', "This was the first mail", ['https://account.live.com/SecurityNotifications/Update']], 
['Second Mail!', 'emailsender2@email.com', '14 Apr 2021 11:33 PM', 'Lorem Ipsum...second mail....', ['https://thatlinkwasinthesecondmail']]]

