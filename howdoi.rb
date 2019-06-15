require 'formula'

class Howdoi < Formula
  include Language::Python::Virtualenv

  homepage 'https://github.com/gleitz/howdoi/'
  url 'https://files.pythonhosted.org/packages/da/ce/65bbb76d2af07b6a64b1e9cac5d4bf48fc26e15222d5e36e162eaaeb4335/howdoi-1.2.0.tar.gz'
  sha256 '5dcef6ac9601b19ee42f5b519981359f4f90f3bb8c41ee025eaf5a42c0b082e3'

  depends_on :python if MacOS.version <= :snow_leopard
  depends_on "libxslt" unless OS.mac?

  resource "Pygments" do
		url "https://files.pythonhosted.org/packages/71/2a/2e4e77803a8bd6408a2903340ac498cb0a2181811af7c9ec92cb70b0308a/Pygments-2.2.0.tar.gz"
		sha256 "dbae1046def0efb574852fab9e90209b23f556367b5a320c0bcb871c77c3e8cc"
	end

  resource "argparse" do
		url "https://pypi.python.org/packages/18/dd/e617cfc3f6210ae183374cd9f6a26b20514bbb5a792af97949c5aacddf0f/argparse-1.4.0.tar.gz"
		sha256 "62b089a55be1d8949cd2bc7e0df0bddb9e028faefc8c32038cc84862aefdd6e4"
	end

  resource "cssselect" do
		url "https://files.pythonhosted.org/packages/52/ea/f31e1d2e9eb130fda2a631e22eac369dc644e8807345fbed5113f2d6f92b/cssselect-1.0.3.tar.gz"
		sha256 "066d8bc5229af09617e24b3ca4d52f1f9092d9e061931f4184cd572885c23204"
	end

  resource "lxml" do
		url "https://files.pythonhosted.org/packages/4b/20/ddf5eb3bd5c57582d2b4652b4bbcf8da301bdfe5d805cb94e805f4d7464d/lxml-4.2.5.tar.gz"
		sha256 "36720698c29e7a9626a0dc802ef8885f8f0239bfd1689628ecd459a061f2807f"
	end

  resource "pyquery" do
		url "https://files.pythonhosted.org/packages/e4/46/596311bb390c902b61499ff9fd5a355cdf85c8455737cb0f08c6c2c13e22/pyquery-1.4.0.tar.gz"
		sha256 "4771db76bd14352eba006463656aef990a0147a0eeaf094725097acfa90442bf"
	end

  resource "requests" do
		url "https://files.pythonhosted.org/packages/40/35/298c36d839547b50822985a2cf0611b3b978a5ab7a5af5562b8ebe3e1369/requests-2.20.1.tar.gz"
		sha256 "ea881206e59f41dbd0bd445437d792e43906703fff75ca8ff43ccdb11f33f263"
	end

  resource "cachelib" do
		url "https://files.pythonhosted.org/packages/e6/5b/39d1f9071e95123a4ae6d8bdeb53416d1af601f662641eac9b0d7c844dba/cachelib-0.1.tar.gz"
		sha256 "8b889b509d372095357b8705966e1282d40835c4126d7c2b07fd414514d8ae8d"
	end

  resource "appdirs" do
		url "https://files.pythonhosted.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-1.4.3.tar.gz"
		sha256 "9e5896d1372858f8dd3344faf4e5014d21849c756c8d5701f78f8a103b372d92"
	end

  resource "urllib3" do
		url "https://files.pythonhosted.org/packages/4c/13/2386233f7ee40aa8444b47f7463338f3cbdf00c316627558784e3f542f07/urllib3-1.25.3.tar.gz"
		sha256 "dbe59173209418ae49d485b87d1681aefa36252ee85884c31346debd19463232"
	end

  resource "chardet" do
		url "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"
		sha256 "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"
	end

  resource "certifi" do
		url "https://files.pythonhosted.org/packages/06/b8/d1ea38513c22e8c906275d135818fee16ad8495985956a9b7e2bb21942a1/certifi-2019.3.9.tar.gz"
		sha256 "b26104d6835d1f5e49452a26eb2ff87fe7090b89dfcaee5ea2212697e1e1d7ae"
	end

  resource "idna" do
		url "https://files.pythonhosted.org/packages/ad/13/eb56951b6f7950cadb579ca166e448ba77f9d24efc03edd7e55fa57d04b7/idna-2.8.tar.gz"
		sha256 "c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407"
	end

  def install
    virtualenv_install_with_resources
  end

  test do
    ENV["LANG"] = "en_US.UTF-8"
    assert_match version.to_s, shell_output("#{bin}/howdoi --version 2>&1")
  end
end
