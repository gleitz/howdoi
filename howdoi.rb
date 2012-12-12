require 'formula'

class Howdoi < Formula
  homepage 'https://github.com/gleitz/howdoi/'
  url 'http://pypi.python.org/packages/source/h/howdoi/howdoi-0.1.2.tar.gz'
  sha1 '26516710ec7b1d0f6b30527b3da424f8b7ba88e8'

  def install
    setup_args = ['setup.py', 'install']
    system "python", *setup_args
  end
end
