require 'formula'

class Howdoi < Formula
  homepage 'https://github.com/gleitz/howdoi/'
  url 'http://pypi.python.org/packages/source/h/howdoi/howdoi-1.1.6.tar.gz'
  sha1 '05e6b539aa566b1f69db0a7c70e2892d28423de4'

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
