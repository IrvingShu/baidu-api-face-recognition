nohup python3 -u ./src/crawler_name_img.py \
    --start-page 5590 \
    --end-page 10000 \
    --save-img-dir ../data/ \
    --save-path ../result/5590_10000.txt \
    > ./5590_10000.log 2>&1 &
