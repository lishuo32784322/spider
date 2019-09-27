def main():
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'red'])

if __name__ == '__main__':
    print('red')
    main()