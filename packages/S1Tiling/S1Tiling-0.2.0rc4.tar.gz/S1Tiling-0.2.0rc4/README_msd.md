# Comment avoir un env de developpement pour S1Tiling

Pré-requis: Ubuntu LTS >= 18.04

1. Récupérer OTB-7.2.0

```sh
wget https://www.orfeo-toolbox.org/packages/OTB-7.2.0-Linux64.run
```

2. Create a virtualenv

```sh
virtualenv venv -p python3
```

3. Installer OTB-7.2.0

```sh
chmod +x OTB-7.2.0-Linux64.run
./OTB-7.2.0-Linux64.run --target venv/otb-7.2.0
# Update the otb python wrapping
source venv/otb-7.2.0/otbenv.profile
ctest -S venv/otb-7.2.0/share/otb/swig/build_wrapping.cmake -VV
# Add a custom gdal-config to otb binaries
cp s1tiling/resources/gdal-config venv/otb-7.2.0/bin/
chmod +x venv/otb-7.2.0/bin/gdal-config
# Update otbenv.profile
echo 'export LD_LIBRARY_PATH=$(cat_path "${CMAKE_PREFIX_PATH}/lib" "$LD_LIBRARY_PATH")' >> venv/otb-7.2.0/otbenv.profile
```

4. Installer l'environnement de dev de s1tiling

```sh
# need to source the env to update the LD_LIBRRARY_APTH
source venv/otb-7.2.0/otbenv.profile
source venv/bin/activate
# need to perform a two step install because gdal need numpy for build wheel
pip install numpy
pip install -r requirements-dev.txt
pip install pylint
```

5. Use the env

```sh
source venv/otb-7.2.0/otbenv.profile
source venv/bin/activate
```
