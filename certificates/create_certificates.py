import os

# Make folder for certificates if it doesn't exist
os.makedirs('svgs', exist_ok=True)

total_hours = 18
minimum = 0.4 #The minimum attendance ratio to consider the course completed

# Read the svg base certificate as text (you can!)
with open('base_certificate.svg', 'r') as f:
    base = f.read()

# Read the list of participants, hours and project flags
with open('participants_hours_project.csv', 'r') as f:
    f.readline() # To skip the headers
    namelist = f.readlines()
for i in range(len(namelist)):
    el = namelist[i][:-1]
    el = el.split(',')
    namelist[i] = el

"""
TEXT REPLACEMENT AND SAVING A CERTIFICATE FOR EACH STUDENT
The base certificate has the formula "attended". We'll leave it for people who didn't
attend at least total_hours*minimum hours, and change it to "completed" for those who
did. In case of course completion, we'll specify the total duration of the course.
Those who also completed the final project will get a special mention about passing the
final assessment.
"""
for student in namelist:
    name = student[0]
    hours = student[1]
    project = student[2]

    # First we write the name
    mod = base.replace('NAMENAME', name)

    # Then let's check attendance and project
    if int(hours) < total_hours*minimum:
        timestring = f'for a total of {hours} hours, '
        mod = mod.replace('for a total of HOURSHOURS hours, ', timestring)
        if project != '1':
            mod = mod.replace(', and passed the final assessment with success.', '.')
    else:
        mod = mod.replace('attended the course', 'completed the 18-hour course')
        mod = mod.replace('for a total of HOURSHOURS hours, ', '')
        if project != '1':
            mod = mod.replace('and passed the final assessment with success.', '')
            mod = mod.replace('Pisa, Italy,', 'Pisa, Italy.')

    # Finally save the svg
    with open('svgs/'+name.replace(' ', '_')+'.svg', 'w') as f:
        f.write(mod)

# NOTE: to convert svg files to pdf in bulk, I use the following bash
# script (outside of this script):
# for i in *.svg;do rsvg-convert -f pdf -o ${i%.*}.pdf $i;done
# It uses the library librsvg2-bin
