pip3 install -r requirements.txt

# Automatically replace the python version. Thanks to @bonelifer for this
version=`python3 -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
sed -i "s/libpython3.10.so/libpython$version.so/g" ./src/plugin.c

rm -rf build
meson build
cd build
sudo meson install
cd ..