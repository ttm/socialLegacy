    def go(self,url):
        """Ensure the browser goes to the link provided"""
        # make async browser visit.
        # each 2 seconds, check if browser is on correct link
        # else restart async process
        pool=mp.Pool(processes=1)
        pool.apply_async(self.browser.visit,args=(url,))
        while 1:
            time.sleep(5)
            if url==self.browser.url:
                break
            else:
                pool.terminate()
                pool=mp.Pool(processes=1)
                pool.apply_async(self.browser.visit,args=(url,))
        pass
