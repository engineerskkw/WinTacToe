from abc import ABC, abstractmethod
import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from bokeh.plotting import figure, output_notebook, show
from bokeh.layouts import column
from bokeh.palettes import magma as palette
from bokeh.models import LinearColorMapper
from bokeh.models import NumeralTickFormatter

from tornado.ioloop import IOLoop
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
import copy
import threading


from reinforcement_learning.agents.auxiliary_utilities import bucketify
from utils.common_utils import return_deepcopy

class BaseAgent(ABC):
    def __init__(self, epsilon_strategy):
        self.episodes_actions_times = [[]]
        self.all_episodes_returns = []

        self.epsilon_strategy = epsilon_strategy
        self.current_epsilon = None

    def update_epsilon(self):
        self.current_epsilon = next(self.epsilon_strategy)

    @abstractmethod
    @return_deepcopy
    def take_action(self, state, allowed_actions):
        """
        Take an action based on the given state and allowed actions.

        Parameters
        ----------
        state : BaseState
            A state of the environment.
        allowed_actions : BaseActionSpace
            A list of the actions that agent can take.

        Returns
        -------
        BaseAction
            An action taken by the agent.
        """
        pass

    @abstractmethod
    def receive_reward(self, reward):
        """
        Give the agent a reward. Should be overridden only in case of the RL BaseAgent

        Parameters
        ----------
        reward : Float
            Reinforcement learning reward.
        """
        pass

    @abstractmethod
    def exit(self, terminal_state):
        """
        This method allows agent to prepare for shutdown.

        It also provide final/termination state of the game/environment.

        Parameters
        ----------
        terminal_state : BaseState
            Terminal state of the environment.
        """
        pass

    @abstractmethod
    def restart(self):
        """
        This method allows agent to prepare for restart of the environment.
        """
        pass

    def save(self, agent_file_path):
        with open(agent_file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(agent_file_path):
        with open(agent_file_path, 'rb') as file:
            agent = pickle.load(file)
        return agent

    def _repr_svg_(self):
        # TODO seamlessly integrate matplotlib plot with ipython _repr_svg_
        self.visualize()

    def visualize(self, bucketing=True):
        if bucketing:
            er_n = len(self.all_episodes_returns)
            er_buckets_number = min(int(np.ceil(0.1*er_n)), 100)
            er_bucket_size = int(er_n/er_buckets_number)
            performance = (np.array(bucketify(self.all_episodes_returns, er_buckets_number, np.mean))+1)/2.0
        else:
            performance = self.all_episodes_returns
        mean_reward = np.mean(self.all_episodes_returns)

        ep_act_times_flatten = [item for sublist in self.episodes_actions_times for item in sublist]
        mean_action_time = np.mean(ep_act_times_flatten)
        if bucketing:
            at_n = len(ep_act_times_flatten)
            at_buckets_number = min(int(np.ceil(0.1*er_n)), 100)
            at_bucket_size = int(at_n / at_buckets_number)
            action_times = bucketify(ep_act_times_flatten, at_buckets_number, np.mean)
        else:
            action_times = ep_act_times_flatten

        performance_f = figure(title='Performance',
                               x_axis_label=f"Episodes buckets ({er_buckets_number} buckets of size {er_bucket_size})",
                               y_axis_label='Percentage of winnings',
                               plot_width=900,
                               plot_height=300,
                               toolbar_location=None,
                               y_range=(-0.1, 1.1))
        performance_f.yaxis.bounds = (0, 1)
        performance_f.yaxis.formatter = NumeralTickFormatter(format='0 %')

        length = len(performance)
        colors = list(palette(int(1.3*length))[:length])
        color_mapper = LinearColorMapper(palette=colors, low=min(performance), high=max(performance))
        performance_f.scatter(range(len(performance)), performance, color={'field': 'y', 'transform': color_mapper})
        performance_f.line(range(len(performance)), performance, color='grey', alpha=0.5)

        action_times_f = figure(title='Action times',
                                x_axis_label=f"Actions buckets ({at_buckets_number} buckets of size {at_bucket_size})",
                                y_axis_label='Mean action time [ms]',
                                plot_width=900,
                                plot_height=300,
                                toolbar_location=None)

        action_times_f.line(range(len(action_times)), np.array(action_times)*10**3, color='blue')

        show(column(performance_f, action_times_f, self.epsilon_strategy.get_figure()))

        # print(f"Number of played episodes: {er_n}")
        print(f"Mean reward: {'{0:0.6f}'.format(mean_reward)}")
        # print(f"Number of taken actions: {at_n}")
        print(f"Mean action time: {'{0:0.6f}'.format(mean_action_time)}")

    def prepare_performance(self, bucketing=True):
        ep_act_times_flatten = [item for sublist in self.episodes_actions_times for item in sublist]
        er_n = len(self.all_episodes_returns)
        if bucketing:
            if er_n == 0:
                performance = []
                action_times = []
                buckets = np.arange(er_n)
                p_x_axis_label = 'No episodes'
                at_x_axis_label = p_x_axis_label
            else:
                buckets_number = min(int(np.ceil(0.1 * er_n)), 100)
                p_bucket_size = int(er_n / buckets_number)  # TODO: floor, ceil
                at_bucket_size = int(len(ep_act_times_flatten) / buckets_number)
                performance = (np.array(bucketify(self.all_episodes_returns, buckets_number, np.mean)) + 1) / 2.0
                action_times = np.array(bucketify(ep_act_times_flatten, buckets_number, np.mean)) * 10 ** 3
                p_x_axis_label = f"{buckets_number} buckets, {p_bucket_size} episodes per each"
                at_x_axis_label = f"{buckets_number} buckets, {at_bucket_size} episodes per each"
                buckets = np.arange(buckets_number)

        else:
            performance = self.all_episodes_returns
            action_times = ep_act_times_flatten
            buckets = np.arange(er_n)
            p_x_axis_label = f"{er_n} Episodes"
            at_x_axis_label = p_x_axis_label

        return buckets, performance, action_times, p_x_axis_label, at_x_axis_label

    def generate_color(self, y):
        length = len(y)
        if length > 0:
            colors = list(palette(int(1.3 * length))[:length])
            color_mapper = LinearColorMapper(palette=colors, low=min(y), high=max(y))
            return {'field': 'performance', 'transform': color_mapper}
        return 'black'

    def performance_figure(self, doc, period_milliseconds, bucketing=True):
        buckets, performance, action_times, p_x_axis_label, at_x_axis_label = self.prepare_performance(bucketing)
        source = ColumnDataSource({'buckets': buckets, 'performance': performance, 'action_times': action_times})

        performance_f = figure(title='Performance',
                   x_axis_label=p_x_axis_label,
                   y_axis_label='Percentage of winnings',
                   plot_width=900,
                   plot_height=300,
                   toolbar_location=None,
                   y_range=(-0.1, 1.1))
        performance_f.yaxis.bounds = (0, 1)
        performance_f.yaxis.formatter = NumeralTickFormatter(format='0 %')
        color = self.generate_color(performance)
        p_scatter = performance_f.scatter(x='buckets', y='performance', color=color, source=source)
        performance_f.line(x='buckets', y='performance', color='grey', alpha=0.5, source=source)

        action_times_f = figure(title='Action times',
                                x_axis_label=at_x_axis_label,
                                y_axis_label='Mean action time [ms]',
                                plot_width=900,
                                plot_height=300,
                                toolbar_location=None)
        action_times_f.line(x='buckets', y='action_times', color='blue', source=source)

        def update():
            buckets, performance, action_times, p_x_axis_label, at_x_axis_label = self.prepare_performance()
            source.data = {'buckets': buckets, 'performance': performance, 'action_times': action_times}
            performance_f.xaxis.axis_label = p_x_axis_label
            action_times_f.xaxis.axis_label = at_x_axis_label
            color = self.generate_color(performance)
            p_scatter.glyph.fill_color = color
            p_scatter.glyph.line_color = color

        doc.add_periodic_callback(update, period_milliseconds)

        return performance_f, action_times_f

    def prepare_epsilon(self):
        if self.epsilon_strategy is None or self.epsilon_strategy.x is None:
            return [], []
        epsilon_x = np.array(range(len(self.epsilon_strategy.x)))
        epsilon_y = np.array(self.epsilon_strategy.y)
        return epsilon_x, epsilon_y

    def epsilon_figure(self, doc, period_milliseconds):
        epsilon_x, epsilon_y = self.prepare_epsilon()
        source = ColumnDataSource({'epsilon_x': epsilon_x, 'epsilon_y': epsilon_y})

        f = figure(title='Epsilon',
                   x_axis_label=f"Episodes",
                   y_axis_label='Epsilon value',
                   plot_width=900,
                   plot_height=300,
                   toolbar_location=None)
        f.line(x='epsilon_x', y='epsilon_y', color='orange', source=source)

        def update():
            epsilon_x, epsilon_y = self.prepare_epsilon()
            source.data = {'epsilon_x': epsilon_x, 'epsilon_y': epsilon_y}

        doc.add_periodic_callback(update, period_milliseconds)

        return f

    def start_dashboard(self, bucketing=True, period_milliseconds=100):
        def make_document(doc):
            doc.title = f"Agent ({self.__class__.__name__}) dashboard"

            performance_figure, action_times_figure = self.performance_figure(doc, period_milliseconds, bucketing)
            epsilon_figure = self.epsilon_figure(doc, period_milliseconds)

            figures = [performance_figure, action_times_figure, epsilon_figure]

            doc.add_root(column(figures))



        apps = {'/': Application(FunctionHandler(make_document))}
        io_loop = IOLoop.current()
        port = 0
        server = Server(applications=apps, io_loop=io_loop, port=port)
        server.start()
        server.show('/')
        t = threading.Thread(name='Agent Dashboard', target=io_loop.start)
        t.start()
