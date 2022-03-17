import os
import json
import utils
import threading

from flask import Flask, request, jsonify, make_response, send_file
from flask_restful import Resource

# Local
import token_manager as tm


token_manager = tm.TokenManager()

class CreateToken(Resource):
    def get(self):
        new_token = token_manager.create_token()
        data = jsonify({
            'new_token': new_token, 
            'expiration': token_manager.token_expiration_map[new_token].isoformat(),
            'success': True})
        return make_response(data, 200)

    def post(self):
        return {"ErrorMessage": "Request should be GET."}, 201

class RemoveImages(Resource):
    def get(self):
        return {"ErrorMessage": "Request should be POST."}

    def post(self):
        data = request.get_json(force=True)
        if 'token' in data:
            token = data['token']
            token_manager.rm_imgs(token)
            data = jsonify({'success': True})
            return make_response(data, 200)
        
        return {"ErrorMessage": "Invalid POST message."}, 201

class AddImages(Resource):
    def get(self):
        return {"ErrorMessage": "Request should be POST."}

    def post(self):
        '''
            Expected json input:
                {
                    'token': <string>
                },
                request.files.getlist("file[]") : {
                    'img1_name' : img1_file,
                    'img2_name' : img2_file,
                    'img3_name' : img3_file,
                }
        '''
        if 'token' in request.form and token_manager.token_exists(request.form['token']) and len(request.files):
            token = request.form['token']
            usr_dir = token_manager.token_corpus_map[token]

            for _, img in request.files.items():
                img.save(os.path.join(usr_dir, img.filename))
            print(f"Successfully saved new images to corpus for token: {token}")

            threading.Thread(target=token_manager.crier.create_database, args=(usr_dir,)).start()  # Intensive task so do in backend.
            token_manager.crier.token_threads.add(token)    # Indicates the index is being created.
            #token_manager.crier.create_database(usr_dir)
            print(f"Starting index job on image corpus for token: {token}")
            #print(f"Indexed image corpus for token: {token}")

            data = jsonify({'success': True})
            return make_response(data, 200)  

        return {"ErrorMessage": "Invalid POST message."}, 201

class SearchDatabase(Resource):
    def get(self):
        return {"ErrorMessage": "Request should be POST."}

    def post(self):
        '''
            Expected json input:
                {
                    'token': <string>
                },
                request.files.getlist("file[]") : {
                    'img_name' : img1_file
                }
        '''
        if 'token' in request.form and token_manager.token_exists(request.form['token']) and len(request.files):
            token = request.form['token']
            corpus_dir = token_manager.token_corpus_map[token]
            search_basename = f"searchimg_{utils.generate_token()}.jpg"
            search_img_path = os.path.join(corpus_dir, search_basename)
            
            for _, img in request.files.items():
                img.save(search_img_path)

            data = None
            if token_manager.crier.engine_available(token):
                #neighbors, images, image_names, distances = token_manager.crier.search(corpus_dir, search_basename)
                neighbors, image_paths, distances = token_manager.crier.search(corpus_dir, search_basename)
                print(f"Search request successfully fulfilled for token: {token}")
                data = jsonify({
                            #'neighbors': neighbors,    # Uncomment if frontend has access to ids.
                            #'image': images,
                            'image_paths': image_paths,
                            'distances': distances[0].tolist(),
                            'success': True
                            })
            else:
                print(f"Search request not fulfilled since engine still indexing from token: {token}")
                data = jsonify({
                            'success': False,
                            'reason': f"Search request not fulfilled since engine still indexing from token: {token}"
                            })

            os.remove(search_img_path)  # Remove the user's file after done searching.


            return make_response(data, 200)  

        return {"ErrorMessage": "Invalid POST message."}, 201

class RetrieveImages(Resource):
    def get(self, token, imgname):
        if token_manager.token_exists(token):
            return send_file(os.path.join(token_manager.token_corpus_map[token], imgname), mimetype='image/jpg')
            
        return {"ErrorMessage": "Invalid GET message."}, 201

    def post(self, token, imgname):
        return {"ErrorMessage": "Request should be GET."}