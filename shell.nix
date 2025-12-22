let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  packages = with pkgs; [
    python3
    python3Packages.venvShellHook
    sops
  ];
  venvDir = ".venv";
  postVenvCreation = ''
    echo "Installing requirements..."
    pip install -r requirements.txt
  '';
}
