# modify mit to apache
for i in `find castle -name '*.py' |grep -v '__init__.py' |grep -v '_demo.py'`; 
do 
    if head -5 $i |tail -1 |grep -q 'Apache'; 
    then 
        echo $i; 
    else 
        cat apache.txt $i |sed -e '16,24d' > ${i}.01;
        mv ${i}.01 ${i}; 
    fi
done 


# update apache
for i in `find castle -name '*.py' |grep -v '__init__.py' |grep -v '_demo.py'`; 
do 
    if head -2 $i |tail -1 |grep -q 'Google'; 
    then 
        sed -i '2d' $i;
    else 
        echo $i; 
    fi
done 



for i in `find castle -name '*.py' |grep -v '__init__.py' |grep -v '_demo.py'`; 
do 
    echo $i;  
done 

