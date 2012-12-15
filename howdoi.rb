require 'formula'

class Howdoi < Formula
  homepage 'https://github.com/gleitz/howdoi/'
  url 'http://pypi.python.org/packages/source/h/howdoi/howdoi-0.2.tar.gz'
  sha1 '69feff9525279641ccbf94995c0a047c5775eac7'

  def install
    setup_args = ['setup.py', 'install']
    system "python", *setup_args
  end
end
