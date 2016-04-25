require 'formula'

class Howdoi < Formula
  homepage 'https://github.com/gleitz/howdoi/'
  url 'https://pypi.python.org/packages/23/2d/9790707eed08c802daee32183e7c98ec2e9797564dad229738b7f178e18e/howdoi-1.1.9.tar.gz'
  sha1 '58d56ca5e652e20035b4869e589539feea5032aa'

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
