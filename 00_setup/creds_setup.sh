#!/bin/bash

# Hardcoded values
profile_name="bedrock"
aws_access_key=""
aws_secret_key=""

# Check if ~/.aws directory exists, if not create it
if [ ! -d "$HOME/.aws" ]; then
    mkdir "$HOME/.aws"
fi

# Check if the profile already exists
if grep -q "\[${profile_name}\]" "$HOME/.aws/credentials"; then
    echo "Profile ${profile_name} already exists!"
else
    # Append the credentials to the file
    echo -e "[${profile_name}]\naws_access_key_id = ${aws_access_key}\naws_secret_access_key = ${aws_secret_key}\n" >> "$HOME/.aws/credentials"
    echo "Credentials added successfully!"
fi
