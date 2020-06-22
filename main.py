# import os,time
# from test_howdoi import format_url_to_filename,HTML_CACHE_PATH

# f = open('test_urls_listeiwoe.txt','r')

# urls = list(set(f.readlines()))


# for url in urls:
#     file_name = format_url_to_filename(url)
#     path = os.path.join(HTML_CACHE_PATH,file_name)
#     if os.path.exists(path):
#         print('already exists!!!!')
#         continue
#     html = _get_result(url)
#     w = open(path,'w')
#     w.write(html)
#     time.sleep(20)
#     print('done processing --->',url)
#     print('file name -->',file_name)

def build_splitter(splitter_character='=',spliter_length=80):
    return '\n' + splitter_character * spliter_length + '\n\n'


def _get_help_instructions():
    instruction_splitter = build_splitter(' ',60)
    query = 'reverse a string in python.'
    instructions = [
        'Here are a few popular howdoi commands ',
        '>>> howdoi {} (default query)',
        '>>> howdoi {} -a (read entire answer)',
        '>>> howdoi {} -n [number] (retrieve n number of answers)',
        '>>> howdoi {} -l (display only a link to where the answer is gotten from',
        '>>> howdoi {} -c (Add colors to the output)',
        '>>> howdoi {} -e (Specify the search engine you want to use e.g google,bing,duckduckgo)'
        ]
    
    instructions = map(lambda s: s.format(query),instructions)

    return instruction_splitter.join(instructions)


print(_get_help_instructions())