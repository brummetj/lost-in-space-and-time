

# load text
filename = '/usr/local/var/lispat/pdf_data/A.6_NIST 800-53 Security and Privacy Controls for Federal Information Systems and Organizations.txt'
file = open(filename, 'rt')
text = file.read()
file.close()

# split into words by white space
words = text.split()


# convert to lower case
words = [word.lower() for word in words]
print(words[:1000])
