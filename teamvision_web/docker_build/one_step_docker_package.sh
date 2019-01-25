rm -rf ./target/one_step_build
mkdir -p ./target/one_step_build
cp -r ./one_step_build ./target
cp -r ../teamvision/ ./target/one_step_build/teamvision
cd ..
cd teamvision_fontend
npm run build
cd ../docker_build
cp -r ../teamvision_fontend/dist ./target/one_step_build/nginx
cp -r ./target/one_step_build/teamvision/teamvision/static ./target/one_step_build/nginx
cp -f ./target/one_step_build/teamvision/settings.py ./target/one_step_build/teamvision/teamvision/
