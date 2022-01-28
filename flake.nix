{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        tomlFile = builtins.readFile ./Cargo.toml;
	      toml = builtins.fromTOML tomlFile;
      in
        {
          defaultPackage = (pkgs.rustPlatform.buildRustPackage {
            name = toml.package.name;
            version = toml.package.version;

            PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig:${pkgs.freetype.dev}/lib/pkgconfig:${pkgs.expat.dev}/lib/pkgconfig:${pkgs.curl.dev}/lib/pkgconfig";
	          nativeBuildInputs = with pkgs; [
	            pkg-config
              gtk4
              glib
	          ];

            buildInputs = with pkgs; [
              freetype
              openssl
              cmake
              llvm
              gnumake
              expat
              fontconfig
              curl
              gettext
              libadwaita
              gtk4
            ] ++ pkgs.lib.optionals stdenv.isDarwin [
              darwin.apple_sdk.frameworks.CoreText
              libiconv
            ];

            cargoSha256 = "Mk4yOOHh3i70JbvxAkOvR2Xpu0V3/UM3ltXMWk5kUW8=";
            
            src = ./.;
          });
        }
    );
}
