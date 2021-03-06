
__author__ = 'Spondon Saha'

import gflags
import logging
import sta.common.utils
from sta.common.bid_container import BidContainer
from sta.common.coalition_tree_base import CoalitionTreeBase
from sta.sta_idastar.tree_node import TreeNode


class CoalitionTree(CoalitionTreeBase):
    """Contains the core logic for the STA IDA* algorithm."""

    def __init__(self, cbt_list):
        """Constructor.

        Arguments:
            cbt_list: A list of task_container.TaskContainer objects which
            contain the list of bid_container.BidContainer objects that were
            submitted for the task.

        Raises:
            None
        """
        self.cbt_list = cbt_list
        self.root = TreeNode('root', [], []) # name, coalition, onPath
        self.root.blocked = False
        # f-limit for use in the IDA-star algorithm: we are trying to maximize
        # our revenue, hence the f-limit starts at zero
        self.f_limit = 0.0
        # declarations below used for statistical data collection
        self.nodecount = 0

    def ConstructTree(self):
        """The main IDA* outer loop.

        This is the main outer loop of the IDA* algorithm, that iteratively
        looks for the winners.

        Arguments:
            None

        Returns:
            Returns the list of winning bids, selected tasks, node-count, etc.
        """
        # START BUILDING THE TREE
        logging.info('-------------------------------------------------------')
        logging.info('<<<<<<<<<<<<< CONSTRUCTING COALITION TREE >>>>>>>>>>>>>')
        logging.info('-------------------------------------------------------')
        solution_found = False
        winners = []
        task_list = []
        g = 0        
        while not solution_found:
            logging.info('     -- Going Depth First --> %s', self.root.name)
            results = self.DfsContour(node=self.root,
                                      cbt_list=self.cbt_list,
                                      winners=winners,
                                      task_list=task_list,
                                      g=0)
            winners, selected_tasks, new_f = results
            logging.info('     -- Coming out of Depth First...')
            if winners:
                solution_found = True
            else:
                # update the flimit to the next highest revenue value
                logging.info('     -- Updating fLimit = %s', self.f_limit)
                self.f_limit = new_f
        logging.info('-------------------------------------------------------')
        logging.info('<<<<<<<< CONSTRUCTING COALITION TREE COMPLETED >>>>>>>>')
        logging.info('-------------------------------------------------------')
        logging.info('WINNING COALITIONS AND TASKS')
        logging.info('Winning coalitions --> %s', winners)
        logging.info('Respective tasks   --> %s', selected_tasks)
        logging.info('Revenue fetched    --> %s', new_f)
        logging.info('Visited States     --> %s', self.nodecount)
        results = {}
        results['winners'] = winners
        results['selected_tasks'] = selected_tasks
        results['new_f'] = new_f
        results['node_count'] = self.nodecount
        return results

    def DfsContour(self, node, cbt_list, winners, task_list, g):
        """The DFS (Depth First Search) Contour algorithm.

        This algorithm recursively inspects each path to find the winning bids
        using the f-limit. For details on the IDA* algorithm, please check
        http://en.wikipedia.org/wiki/IDA*

        Arguments:
            node: the current node in the IDA* tree.
            cbt_list: list of task-container nodes with bid data.
            winners: current list of winners.
            task_list: list of tasks covered so far.
            g: the total revenue so far.

        Returns:
            The set of winners, the tasks that have been chosen to be
            accomplished and the total revenue/cost of accomplishing all
            these tasks.
        """
        logging.info('-------------------------------------------------------')
        logging.info('    -- Estimating heuristic for node %s', node.name)
        hF = self.EstimateHeuristic(self.cbt_list,
                                    node.coalitions_on_path,
                                    node.all_tasks_on_path,
                                    0)
        logging.info('    -- Heuristic for node %s is %s', node.name, hF)
        logging.info('    <** f-limit = %s, (g + hF) = %s **>', self.f_limit,
                     (g + hF))
        # 1. pruning
        if (g + hF) < self.f_limit:
            logging.info('    (g + hF) is < f-limit....pruning.....')
            return [], [], (g + hF)
        else:
            logging.info('    (g + hF) is >= f-limit....go deeper.....')
        # 2. check if there are any more tasks to handle, then get
        # eligible children
        if cbt_list:
            children = self.GetEligibleChildren(cbt_list[0].GetBidList(),
                                                node.robots_on_path)
        else:
            logging.info('    End of path reached. f-Limit = %s', self.f_limit)
            logging.info('    End of path reached. Winners = %s and g = %s',
                         winners, g)
            logging.info('    -- updating f-limit from %s to %s',
                         self.f_limit, g)
            # revert to branch and bound once the first leaf is reached
            self.f_limit = g
            return winners, task_list, g
        # 3. If there are any eligible children for the current path, then add
        # dummy node and prepare for DFS
        if children or (not children and (len(cbt_list) > 1)):            
            task_name = cbt_list[0].task_name
            # add a dummy node if the children do not belong to the last task
            if len(cbt_list) > 1:
                logging.info('    -- Adding Dummy node to list of children...')
                dummy = BidContainer([], 0)
                children.append(dummy)  # add the dummy node
            logging.info('    Children to be added to %s are %s', node.name,
                         map(lambda(x): x.GetCoalition(), children))
        else: # end of path reached
            logging.info('    End of path reached. f-Limit = %s', self.f_limit)
            logging.info('    End of path reached. Winners = %s and g = %s',
                         winners, g)
            logging.info('    -- updating f-limit from %s to %s',
                         self.f_limit, g)
            # revert to branch and bound once the first leaf is reached
            self.f_limit = g
            return winners, task_list, g
        # 4. Initialize recursion parameters
        max_revenue = 0
        best_winners = []
        list_of_tasks = []
        next_f = 0
        # 5. For each child in children, recursively inspect using heuristics
        # to see if the path is feasible as per f-limit
        for child in children:
            logging.info('        - - - - - - - - - - - - - - - - - - - - - - ')
            logging.info('        -- Adding child node: %s to coalition %s',
                         child.GetCoalition(), node.name)
            self.nodecount += 1
            logging.info('        -- VISITING NEW STATE %s',
                         child.GetCoalition())
            # add a child node and return it's instance
            child_node = self.AddChild(node, child, task_name)
            # recursively inspect the current child
            rest_of_cbtlist = cbt_list[1:]
            new_winners = winners + [child.GetCoalition()]
            new_tasklist = task_list + [task_name]
            new_g = g + int(child.GetBidValue())
            solution, tasks, new_f = self.DfsContour(child_node,
                                                     rest_of_cbtlist,
                                                     new_winners,
                                                     new_tasklist,
                                                     new_g)
            logging.info('        -- returning from DFS contour to node %s ...',
                         node.name)
            if solution and (new_f > max_revenue):
                logging.info('        ** updating max_revenue from %s to %s',
                             max_revenue, new_f)
                logging.info('        ** updating best_winners from %s to %s',
                             best_winners, solution)
                max_revenue = new_f
                best_winners = solution
                list_of_tasks = tasks
            else:
                logging.info(('        ** NO NEED TO UPDATE: solution = %s, '
                              'max_revenue = %s, new_f = %s'),
                              solution, max_revenue, new_f)
            logging.info('        $$ updating next_f from %s to %s',
                         next_f, new_f)
            next_f = max(next_f, new_f)
        # 6. return results, curl back up the recursion stack
        if best_winners:
            return best_winners, list_of_tasks, max_revenue
        else:
            return [], [], next_f

    def AddChild(self, parent_node, child, task_name):
        """Creates a TreeNode object and assigns the necessary data to it.

        Arguments:
            parent_node: the parent TreeNode object stored in child.parent
            child: the child TreeNode object that we are at.
            task_name: The task name that the current child object is associated
            to. Essentially, the child node is the bid that was submitted for
            this particular task.

        Returns:
            Returns either a dummy node or a child TreeNode object.

        Raises:
            None
        """
        # fetch the child coalition and bid value from the coalitionNode object
        coalition = child.GetCoalition()
        bid_value = child.GetBidValue()
        if coalition: # its a regular coalition with a positive bid value
            childNode = TreeNode(str(coalition), coalition,
                                 parent_node.robots_on_path + coalition)
            childNode.parent = parent_node
            # deep copy the entire list
            childNode.coalitions_on_path = parent_node.coalitions_on_path[:]
            # extra operation than DUMMY
            childNode.coalitions_on_path.append(coalition)
            childNode.total_revenue = parent_node.total_revenue + int(bid_value)
            # deep copy the entire list
            childNode.tasks_on_path = parent_node.tasks_on_path[:]
            # extra operation than DUMMY
            childNode.tasks_on_path.append(task_name)
            childNode.member_of_task = task_name
            childNode.all_tasks_on_path = parent_node.all_tasks_on_path[:]
            childNode.all_tasks_on_path.append(task_name)
            # add the child node as a child of the parent node
            #parent_node.children.append(childNode)
            return childNode
        else: # dummy node with an empty coalition set and a zero bid value
            dummyNode = TreeNode('dummy', [], parent_node.robots_on_path)
            dummyNode.parent = parent_node
            dummyNode.coalitions_on_path = parent_node.coalitions_on_path[:]
            dummyNode.total_revenue = parent_node.total_revenue
            dummyNode.tasks_on_path = parent_node.tasks_on_path
            dummyNode.member_of_task = task_name
            dummyNode.all_tasks_on_path = parent_node.all_tasks_on_path[:]
            dummyNode.all_tasks_on_path.append(task_name)
            return dummyNode
