from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import random

def create_graph_as_png(names, values, games_played, games_won, good_letters_guessed, letter_guessed, user):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure()

    fig.suptitle('Your data')

    ax1 = fig.add_subplot(gs[0,:])

    ax1.bar(names, values, color=colors[random.randrange(len(colors))])

    title = "Number of times {} used each letter".format(user.name)

    ax1.set_title(title)

    labels = ['Lettres ratés', 'lettres devinées']

    sizes = [letter_guessed - good_letters_guessed, good_letters_guessed]

    explode = (0, 0.2)

    ax2 = fig.add_subplot(gs[1,0])

    ax2.pie(sizes, explode=explode, labels=labels, startangle=45, shadow=True)

    labels = ['Games perdues', 'Games gagnées']

    sizes = [games_played - games_won, games_won]

    explode = (0, 0.2)

    ax3 = fig.add_subplot(gs[1,1])

    ax3.pie(sizes, explode=explode, labels=labels, startangle=45, shadow=True)

    file_name = "{}_graph_image.png".format(user.name)
    #plt.show()
    plt.savefig(file_name)
    print("image created")

