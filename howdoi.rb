require 'formula'

class Howdoi < Formula
  homepage 'https://github.com/gleitz/howdoi/'
  url 'http://pypi.python.org/packages/source/h/howdoi/howdoi-1.1.1.tar.gz'
  sha1 '98e8b302fb02ae26f630682662247afe78fb4553'

  def install
    setup_args = ['setup.py', 'install']
    system "python", *setup_args
  end

  def scripts_folder
    HOMEBREW_PREFIX/"share/python"
  end

  def caveats
    <<-EOS.undent
      To run the `howdoi` command, you'll need to add Python's script directory to your PATH:
        #{scripts_folder}
    EOS
  end
end
