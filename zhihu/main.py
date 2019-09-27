def main():
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'zhihu_user'])

if __name__ == '__main__':
    print(1)
    main()