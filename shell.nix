let
    pkgs = import <nixpkgs> {};
    config-graph = pkgs.python312.pkgs.buildPythonPackage rec {
        name = "precice-config-graph";
        src = pkgs.fetchFromGitHub {
            owner = "precice-forschungsprojekt";
            repo = "config-graph";
            rev = "master"; # TODO: Set a fixed version "refs/tags/v${version}";
            hash = "sha256-QKqOncz4r7YOdaO1Hem5egSISBjraku8ISOLKMvZIkc=";
        };
        pyproject = true;

        propagatedBuildInputs = with pkgs.python312.pkgs; [
            setuptools
            poetry-core

            lxml
            elementpath
            matplotlib
            networkx
            pytest
        ];
    };
    pyprecice = pkgs.python312.pkgs.buildPythonPackage rec {
        pname = "pyprecice";
        version = "3.1.2";
        format = "setuptools";

        disabled = pkgs.python312.pkgs.pythonOlder "3.7";

        src = pkgs.fetchFromGitHub {
            owner = "precice";
            repo = "python-bindings";
            rev = "refs/tags/v${version}";
            hash = "sha256-/atuMJVgvY4kgvrB+LuQZmJuSK4O8TJdguC7NCiRS2Y=";
        };

        buildInputs = with pkgs; [
            python312Packages.setuptools
        ];

        nativeBuildInputs = with pkgs.python312.pkgs; [
            setuptools
            pip
            cython
            pkgconfig
        ];

        propagatedBuildInputs = with pkgs; [
            python312Packages.numpy
            python312Packages.mpi4py
            python312Packages.setuptools
            precice
        ];

        # Disable Test because everything depends on open mpi which requires network
        doCheck = false;

        # Do not use pythonImportsCheck because this will also initialize mpi which requires a network interface

        meta = with pkgs.lib; {
            description = "Python language bindings for preCICE";
            homepage = "https://github.com/precice/python-bindings";
            license = licenses.lgpl3Only;
            maintainers = with maintainers; [ Scriptkiddi ];
        };
    };
    pythonEnv = pkgs.python312.withPackages(ps: [
        config-graph
        pyprecice
        pkgs.python312Packages.pytest
    ]);
in pkgs.mkShell {
    packages = [
        pythonEnv
    ];
    nativeBuildInputs = with pkgs; [
        python312Packages.setuptools
    ];
    shellHook = ''
        # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
        # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
        export PIP_PREFIX=$(pwd)/_build/pip_packages
        export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PWD:$PYTHONPATH"
        export PATH="$PIP_PREFIX/bin:$PATH"
        unset SOURCE_DATE_EPOCH
    '';
}
