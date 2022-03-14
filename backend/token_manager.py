import os
import shutil
import datetime
import threading

# Local
import utils
import model
import model_defs

# Important constants.
TMP_CORPUS_DIR = "tmp_corpus"
EXPIRATION_DELTA = datetime.timedelta(seconds=1800)    # Half Hour until expiration
TOKEN_CLEANER_DELTA = 60    # Clean up stale tokens every minute

EXAMPLE_IMG_CORPUS_DIR = "example_image_corpus" # change
NUM_RESULTS = 10                                # change
MODEL_NAME = "efficientnetv2-s"                 # change (maybe?)   

model_handle = model_defs.MODEL_HANDLE_MAP.get(MODEL_NAME)
pixels = model_defs.MODEL_IMAGE_SIZE_MAP.get(MODEL_NAME)
IMAGE_SIZE = (pixels, pixels)
#BATCH_SIZE = 16 # Not needed

print(f"Selected model: {MODEL_NAME} : {model_handle}")
print(f"Input size {IMAGE_SIZE}")
print(f"Num results: {NUM_RESULTS}")
print(f"Temp directory: {TMP_CORPUS_DIR}")

# Manages user tokens and their associated data.
class TokenManager(object):
    def __init__(self):
        self.tokens = set()
        self.token_corpus_map = dict()
        self.token_expiration_map = dict()

        self.crier = model.CRIER(MODEL_NAME, IMAGE_SIZE, NUM_RESULTS)

        self.reset_tmp_dir()
        os.mkdir(TMP_CORPUS_DIR)
        self.__start_token_cleaner()

    # Returns boolean if provided string token exists.
    def token_exists(self, token):
        return token in self.tokens

    # Creates a new token a returns it to the user.
    # Byproduct is a temporary storage that will expire in 60 minutes.
    def create_token(self):
        new_token = utils.generate_token()
        new_usr_dir = os.path.join(TMP_CORPUS_DIR, new_token)
        os.mkdir(new_usr_dir)

        self.tokens.add(new_token)
        self.token_corpus_map.update({ new_token: new_usr_dir })
        self.token_expiration_map.update({ new_token: (datetime.datetime.now() + EXPIRATION_DELTA) })
        self.crier.create_engine(new_usr_dir)

        print(f"Created engine and directory for token: {new_token}")

        return new_token        

    # Removes a provided token. If token doesn't exist, does nothing.
    def remove_token(self, token):
        if not self.token_exists(token): return

        self.tokens.remove(token)
        self.token_corpus_map.pop(token, None)
        self.token_expiration_map.pop(token, None)

        dir_to_rm = os.path.join(TMP_CORPUS_DIR, token)
        self.crier.delete_engine(dir_to_rm)
        shutil.rmtree(dir_to_rm)

    # Removes a users' images and reset's their engine. If token doesn't exist, does nothing.
    def rm_imgs(self, token):
        if not self.token_exists(token): return

        dir_to_rm = self.token_corpus_map[token]
        self.crier.delete_engine(dir_to_rm)
        shutil.rmtree(dir_to_rm)

        os.mkdir(dir_to_rm)     # We still want the database.
        self.crier.create_engine(dir_to_rm)

        print(f"Successfully reset engine and cleared image corpus for token: {token}")

    # Returns true if the token is stale, false otherwise. If token doesn't exist, return false.
    def is_token_stale(self, token):
        if not self.token_exists(token): return false

        return self.token_expiration_map[token] < datetime.datetime.now()

    # Removes stale tokens.
    def clean_stale_tokens(self):
        for token in self.tokens:
            if self.is_token_stale(token):
                print(f"Found stale token: {token}")
                remove_token(token)
                print(f"Successfully removed stale token: {token}")

    def reset_tmp_dir(self):
        if os.path.exists(TMP_CORPUS_DIR): shutil.rmtree(TMP_CORPUS_DIR)

    # Looks for stale tokens and removes them.
    def __start_token_cleaner(self):
        threading.Timer(TOKEN_CLEANER_DELTA, self.clean_stale_tokens).start()