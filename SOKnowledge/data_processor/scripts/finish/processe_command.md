## 1. import from StackOverflow dump xml file
use db_import_xml.py
generate one table-- remove_tag_posts_body


## 2. remove html tag and extract code in code tag for post body
generate two table-- remove_tag_posts_body,post_code_block
```
    python db_remove_tag.py 2000 2000 E:\laboratory\StackOverflow\SOKnowledge\SOKnowledge\db
```
## 3. tokenize posts body text
generate one table-- tokenize_RemoveTagBody_for_remove_tag_posts_body
example:
```
python db_tokenize_text.py remove_tag_posts_body RemoveTagBody --dump-path E:\laboratory\StackOverflow\SOKnowledge\SOKnowledge\db
```
## 4. tokenize code block text
generate one table-- tokenize_codeBlock_for_posts_code_body

ps:the primary key name for code block is 'id',not 'Id'

example:
```
python db_tokenize_text.py posts_code_block codeBlock --dump-path E:\laboratory\StackOverflow\SOKnowledge\SOKnowledge\db --primary-key-name id
```
## 5. join the tokenize code to old table

join the tokenize code to old table with the original code block table

that is ,tokenize_codeBlock_for_posts_code_body inner join posts_code_block
and drop posts_code_block
```
python db_join_tokenize_code_with_old_table.py E:\laboratory\StackOverflow\SOKnowledge\SOKnowledge\db
```