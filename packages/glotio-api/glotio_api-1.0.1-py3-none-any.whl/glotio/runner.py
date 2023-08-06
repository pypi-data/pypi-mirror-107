"""
runner function of glot.io API
"""

import json

import requests


class Runner:
    """glot.io API Runner class"""

    API_URL = "https://glot.io/api/run"
    token = None
    lang_name = None
    parameter = {
        "files": [],
    }
    lang_file_extension_dict = {
        "python": "py",
        "assembly": "asm",
        "ats": "ast",
        "bash": "sh",
        "c": "c",
        "clojure": "clj",
        "cobol": "cbl",
        "coffeescript": "coffee",
        "cpp": "cpp",
        "crystal": "cr",
        "csharp": "cs",
        "d": "d",
        "elixir": "ex",
        "elm": "elm",
        "erlang": "hrl",
        "fsharp": "fs",
        "go": "go",
        "groovy": "groovy",
        "haskell": "hs",
        "idris": "idr",
        "java": "java",
        "javascript": "js",
        "julia": "jl",
        "kotlin": "kt",
        "lua": "lua",
        "mercury": "m",
        "nim": "nim",
        "nix": "nix",
        "ocaml": "ml",
        "perl": "pl",
        "php": "php",
        "python": "py",
        "raku": "raku",
        "ruby": "rb",
        "rust": "rs",
        "scala": "scala",
        "swift": "swift",
        "typescript": "ts",
    }

    def __init__(self, token):
        """
        set glot.io API token
        """
        self.token = token

    def get_lang():
        """
        get language list
        """
        res = requests.get("https://glot.io/api/run").json()
        lang_dict = {e["name"]: e["url"] for e in res}  # langname: url

        return lang_dict

    def set_lang(self, lang):
        """
        set language name
        """
        if lang not in Runner.get_lang().keys():
            raise GlotIOError(f"Language '{lang}' is not found.")
        else:
            self.lang_name = lang

    def set_stdin(self, arg):
        """
        set stdin buffer
        """
        self.parameter["stdin"] = arg

    def set_command(self, arg):
        """
        set command to execute
        """
        self.parameter["command"] = arg
    
    def set_code(self, code, filename=None):
        """
        set main source code
        """
        if filename is None:
            if self.lang_name is None:
                raise GlotIOError("Language must be set first.")
            else:
                filename = "Main." + self.lang_file_extension_dict[self.lang_name]
                if filename in [f["name"] for f in self.parameter["files"]]:
                    raise GlotIOError(f"File '{filename}' already exists.")

        self.parameter["files"].append({"name": filename, "content": code})

    def run(self):
        """
        excute on glot.io
        """
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Token {self.token}", 
        }

        payload = json.dumps(self.parameter)
        r = requests.post(self.API_URL + "/" + self.lang_name + "/latest", data=payload, headers=headers)
        r.raise_for_status()

        return r.json()


class GlotIOError(Exception):
    """Exception class that signals that an error has occurred in the GlotIO class"""
    pass


if __name__ == "__main__":
    g = Runner("[YOUR_API_KEY]")
    print(Runner.get_lang().keys())
    g.set_lang("python")
    code = "import sys;print(input() + ', ' + sys.argv[1])"
    g.set_code(code, filename="main.py")
    g.set_stdin("input text")
    g.set_command("python3 main.py 'command line argument'")
    result = g.run()
    print(result)
