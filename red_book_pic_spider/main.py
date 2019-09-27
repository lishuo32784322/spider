def main():
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'pic'])

if __name__ == '__main__':
    print('red_pic')
    main()