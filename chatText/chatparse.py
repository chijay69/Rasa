import os

# Define the directory where your conversation log files are located
log_directory = '.\chatTXT'

# Iterate through each file in the directory
for filename in os.listdir(log_directory):
    if filename.endswith(".txt"):  # Adjust the file extension as needed
        with open(os.path.join(log_directory, filename), 'r', encoding='latin-1') as file:
            lines = file.readlines()

        # Create a new list to store the modified lines
        new_lines = []

        # Flag to track if the first line should be removed
        remove_first_line = True

        # Iterate through each line in the file
        for line in lines:
            # Check if the line contains the specified message
            if "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more." in line and remove_first_line:
                remove_first_line = False
                continue  # Skip the first line

            # Check if the line contains the expected timestamp format
            if ' - ' in line:
                # Delete the timestamp string
                line = line.split(' - ', 1)[1]  # Split the line and keep the part after the timestamp
                new_lines.append(line)

        # Write the modified lines back to the file
        with open(os.path.join(log_directory, filename), 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

print("Processing completed.")
