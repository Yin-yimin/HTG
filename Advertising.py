import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(100)


class AB_testing():
    def __init__(self, filename):
        self.result = {
            0: {'buy': 0, 'not_buy': 0},
            1: {'buy': 0, 'not_buy': 0},
            2: {'buy': 0, 'not_buy': 0},
            3: {'buy': 0, 'not_buy': 0},
            4: {'buy': 0, 'not_buy': 0},
            5: {'buy': 0, 'not_buy': 0},
            6: {'buy': 0, 'not_buy': 0},
            7: {'buy': 0, 'not_buy': 0},
            8: {'buy': 0, 'not_buy': 0},
        }

        self.cvr = {
            0:[],
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[],
            8:[]
        }

        self.customer = np.loadtxt(filename)
        self.N=len(self.customer)
        self.version=len(self.customer[0])

    def sample(self):
        """picks a version of advertisement randomly"""
        ad_sample = random.randint(0,8)     # 选择的概率均等 [0，8]
        # print(f'choose the version of advertisement: {ad_sample}')
        return ad_sample

    def update_result(self):
        """updates the self.result and self.cvr based on the purchasing outcome of each customer"""
        for i in range(self.N):      # how many customers in all
            # update randomly
            ad_sample = self.sample()

            # update purchasing data
            if self.customer[i][ad_sample] == 1:        
                self.result[ad_sample]['buy'] += 1
            else:
                self.result[ad_sample]['not_buy'] += 1
            # calculate
            for v in range(self.version):
                if v == ad_sample:
                    rate = self.result[v]['buy']/(self.result[v]['buy']+self.result[v]['not_buy'])
                else:
                    if self.cvr[v] == []: rate=0
                    else: rate = self.cvr[v][-1]
                self.cvr[v].append(rate)

    def best(self):
        """Return the best version of advertisement"""
        # 不同广告版本的最新转化率
        cvr_update = list(self.cvr[i][-1] for i in range(self.version))
        # 选择列表最大值对应的index
        ad_best = cvr_update.index(max(cvr_update))
        return ad_best

    def draw(self,x_range,title):
        for i in range(0, self.version):
            plt.plot(range(0, x_range), list(self.cvr.values())[i][:x_range], label=i)
            plt.legend()
            plt.xlabel('Number of Customers', fontsize=12)
            plt.ylabel('Conversion Rate', fontsize=12)
        plt.savefig(title)




class Thompson_sampling(AB_testing):

    def sample(self):
        """picks a version of advertisement using Thompson sampling algorithm"""
        beta_list = []
        for j in range(self.version):
            ad_beta = np.random.beta(self.result[j]['buy']+1,self.result[j]['not_buy']+1)
            beta_list.append(ad_beta)
        ad_sample = beta_list.index(max(beta_list))
        # print(f'choose the version of advertisement: {ad_sample}')
        return ad_sample


if __name__=="__main__":
    a=AB_testing('custumer.txt')
    a.update_result()
    plt.figure(0)
    a.draw(2000,'AB_Testing.png')


    t=Thompson_sampling('custumer.txt')
    t.update_result()
    plt.figure(1)
    t.draw(2000,'Thompson_Sampling.png')

    print('The best version is:')
    print('AB Testing Result:', a.best())
    print('Thompson Sampling Result:', t.best())