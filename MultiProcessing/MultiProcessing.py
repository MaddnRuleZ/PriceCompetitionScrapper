import multiprocessing

from Utilities import GeneralUtils


# todo make the function passed for single thread variable
class MultiProcessing:

    def init_multiprocessing(self, url_list):
        print("Init Multiprocessing")

        with multiprocessing.Pool(processes=20) as pool:
            index = list(enumerate(url_list, start=1))
            chunk_size = 4  # todo change Chunk Size

            for i in range(0, len(index), chunk_size):
                chunk = index[i:i + chunk_size]

                # todo Change here the Parameters for the Single Thread Function vvvv
                processes = [pool.apply_async(self.single_thread, args=(url,)) for _, url in chunk]
                for process in processes:
                    process.get()

                percentage = GeneralUtils.calculate_percentage(i + chunk_size, len(index))
                print("------------------------------------------------------------------------------------------")
                print("")
                GeneralUtils.display_progress_bar(percentage)
                print("")
                print("------------------------------------------------------------------------------------------")

    def single_thread(self, url):
        print("Starting Thread " + url)


    def finnish_msg(self, result):
        print("Finnished URL ----------------------")
        print(result)
        print("------------- ----------------------")
