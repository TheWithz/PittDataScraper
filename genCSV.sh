#!/bin/bash

# the current time
TIME=$(date +%F_%T)
# select halls from database
HALLS=$(psql -d pittData -c "(SELECT DISTINCT hall FROM laundrysimple)" -U postgres)
# Turn HALLS into an array
ARR=(`echo ${HALLS}`)
# temp dir for permission issue handling
TEMP_DIR=/tmp/csv_files
# final resting place for the csv
DIR=/run/media/thewithz/LinuxData/csv_files
# loop on the array but not the first item
for HALL in {2..9}; do
    if [ $HALL -ge 2 ] || [ $HALL -le 9 ]
    then
        echo $HALL
        touch $TEMP_DIR/${ARR[$HALL]}$TIME.csv
        chmod 777 $TEMP_DIR/${ARR[$HALL]}$TIME.csv
        # pull from hall and export to csv from database
        psql -d pittData -c "COPY (SELECT * FROM laundrysimple WHERE hall='${ARR[$HALL]}') TO '$TEMP_DIR/${ARR[$HALL]}$TIME.csv' WITH CSV HEADER DELIMITER ','" -U thewithz
    fi
done
# move from temp directory to the HDD
mv $TEMP_DIR/* $DIR
# move empty files to trash
find $DIR/* -size  0 -exec mv {} ~/Trash \;
# move files older than 30 days to trash
find $DIR/* -mtime +30 -exec mv {} ~/Trash \;
