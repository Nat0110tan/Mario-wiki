/* Zach's General Thoughts 
    id's for each table should be an integer identifier, and they 
    should be auto-incrementing for unique identification. 
*/

-- Create an index to speed up our full text search --
CREATE INDEX raw_text_search_idx on posts USING GIN (to_tsvector('english', raw_text));

-- refers to either a main post or a discussion post --
CREATE TABLE posts(
    id SERIAL,
    user_id VARCHAR(128) NOT NULL,
    title VARCHAR(64) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(64) NOT NULL, 
    post_date TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    post_type VARCHAR(16) NOT NULL, -- either POST or DISCUSSION --
    likes INT NOT NULL DEFAULT 0,
    raw_text TEXT NOT NULL default "",
    PRIMARY KEY (id)
);
-- post can belong to one category --
/* Planned Categories
    - Games
    - Characters
    - Platforms
    - Species?
*/
/* Zach's Thoughts 
    I don't know if we'll need a table for the categories.
    Unless we are planning on having users create categories.
    We should be able to just store the category in the 
    sub-categories table, then query it with 
        'select * from posts_sub_categories where category=___'
*/
/*
CREATE TABLE posts_categories(
    post_id INT NOT NULL,
    category_title VARCHAR(64) NOT NULL,
    PRIMARY KEY (post_id)
);
*/
-- post can belong to many sub-categories --
CREATE TABLE posts_sub_categories(
    post_id INT NOT NULL,
    sub_category_title VARCHAR(64) NOT NULL,
    PRIMARY KEY (post_id, sub_category_title),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

/* Zach's Thoughts 
    I feel like maybe we could just treat replies as other comments.
    We would just have the post_id be the previous comment.
    And we should only allow replies to the original comments. Like
    if a user makes a comment on a post, then someone could reply to
    that comment, but then those replies cannot have further replies.
*/
CREATE TABLE post_comments(
    id SERIAL NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    post_id INT NOT NULL,
    content TEXT NOT NULL,
    post_date TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    revision_date TIMESTAMP,
    likes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);
-- not sure the best way to do replies. Could just store it like below and then for main comments grab all comments belonging to a post not present in this table,
-- then grab any replies belonging to each comment loaded using this table --
/*
CREATE TABLE comment_replies(
    original_id INT NOT NULL,
    reply_id INT NOT NULL,
    PRIMARY KEY (original_id, reply_id)
)
*/

CREATE TABLE category(
    title VARCHAR(64) NOT NULL,
    description TEXT,
    photo VARCHAR(256),
    PRIMARY KEY (title)
);

CREATE TABLE sub_category(
    parent_title VARCHAR(64) NOT NULL,
    subtitle VARCHAR(64) NOT NULL,
    photo VARCHAR(256),
    PRIMARY KEY (parent_title, subtitle),
    FOREIGN KEY (parent_title) REFERENCES category(title)
);

/* Zach's Thoughts 
    user_id should just be an integer identifier, then we can have 
    a separate field if we need a varchar
*/
CREATE TABLE users(
    user_id VARCHAR(128) NOT NULL,
    username VARCHAR(32) NOT NULL, --will need to enforce uniqueness--
    photo_url VARCHAR(256),
    bio TEXT,
    -- level system could be added; each time posting/liking/commenting increases your level --
    -- photo and username can seemingly be stored by auth0 --
    PRIMARY KEY (user_id)
);

CREATE TABLE user_followers(
    user_id VARCHAR(128) NOT NULL,
    follower_id VARCHAR(128) NOT NULL,
    PRIMARY KEY (user_id, follower_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE post_likes(
    post_id INT NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    PRIMARY KEY (post_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
