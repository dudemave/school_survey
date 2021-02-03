import seaborn as sns

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as mcl

from collections import namedtuple, OrderedDict



votes         = None
votes_2nd     = None

header        = None
header_2nd    = None

global_threshold     = 4
global_threshold_2nd = 1


global_class_list = [
    '1a', '1b', '1c', '1d', '1e',
    '2a', '2b', '2c', '2d', 
    '3a', '3b', '3c', '3d', 
    '4a', '4b', '4c', '4d',
    '5a', '5b', '5c', '5d', '5e',
    '6a', '6b', '6c', '6d',
]


a4_landscape = (11.69,8.27)
a4_portrait  = tuple(reversed(a4_landscape))


# colors 
default_blue    = '#1F77B4'
default_orange  = '#FF7F0E'
default_brown   = '#8c564b'
default_green   = '#2CA02C'
default_red     = '#D62728'
default_grey    = '#7f7f7f' #'tab:grey'

# https://matplotlib.org/3.1.0/users/dflt_style_changes.html#colors-in-default-property-cycle


def spaceless(my_string : str) -> str:

    spaceless = my_string.replace("?", "")
    spaceless = spaceless.strip()
    spaceless = spaceless.replace(" ", "_")
    spaceless = spaceless.replace("/", "_")

    return spaceless


def break_long_title(title : str, max_length: int = 30)  -> str:
    
    
    split_pos_list = [0] # to avoid index out of range
    
    SearchRange  = namedtuple('search_range', ['start', 'end'])
    search_range = SearchRange(0, max_length)

    while len(title) > search_range.end :
        split_pos = title.rfind(' ', search_range.start, search_range.end)

        # no space found in range
        if (split_pos == split_pos_list[-1] or
            split_pos == -1):
            search_range = SearchRange(search_range.start, search_range.end + max_length)
            
        else:
            # eventually reset
            split_pos_list.append(split_pos)
            search_range = SearchRange(split_pos , split_pos + max_length)
        
    split_pos_list.pop(0)
    split_title_list = list(title)

    # remove first item since it was set to 0

    for split_pos in split_pos_list:
        split_title_list[split_pos] = '\n'    

    split_title=''.join(split_title_list)

    return split_title


def plot_title(class_id, title):
    if class_id == 'all':
        plot_title =  title + ' - alle Klassen'
    elif len(class_id ) == 1:
        plot_title =  title + f' - Klassenstufe {class_id}'
        
    else:
        plot_title =  title + f' - Klasse {class_id}'
    
    return plot_title



def generate_file_name(title: str, class_id:str = all, 
                       file_format: str = 'pdf', sub_page_nr:int = 0) -> str :

    if sub_page_nr != 0:
        title = f"{title}_{sub_page_nr:02d}"

    if class_id == 'all':
        fig_file_name = 'Alle_Klassen_' + title
    elif len(class_id) == 1:
        fig_file_name = 'Klassenstufe_%s_' %class_id + title
        
        
    else:
        fig_file_name = 'Klasse_%s_' %class_id + title
    
    file_name = f'{spaceless(fig_file_name)}.{file_format}' 
    
    return file_name


def load_data_general(class_id: str = 'all') -> pd.DataFrame :
    
    global votes
    global votes_2nd

    global header 
    global header_2nd 

    votes     = pd.read_csv('Distanzunterricht_20210122.csv')
    votes_2nd = pd.read_csv('Fragebogen zur Umsetzung des Distanzlernkonzepts (18.1.-22.1.2021).csv')

    header=votes.columns.values
    header_2nd=votes_2nd.columns.values

    # TODO: raise error if invalid class id

    if class_id == 'all':
        class_data     = votes
        class_data_2nd = votes_2nd

    # get data of all classes of the same level (e.g all first grade students) 
    elif class_id in [str (ii) for ii in range(1,7)]:
 
        classes_in_level = get_classes_of_level(class_id) # TODO: remove hard coded

        class_data     = votes    [votes    [header    [1]].isin(classes_in_level)]
        class_data_2nd = votes_2nd[votes_2nd[header_2nd[1]].isin(classes_in_level)]
        
    # get data of a specific class
    else: 
        class_data     = votes    [votes    [header    [1]] == class_id]
        class_data_2nd = votes_2nd[votes_2nd[header_2nd[1]] == class_id]

        # enought_answers_for_this_class    
        # len(data) would do the job # but nan would be counted
        
        counts     = (class_data[header[1]]==class_id).sum()
        counts_2nd = (class_data_2nd[header_2nd[1]]==class_id).sum()

        print (f'Klasse {class_id} - stats answers: {counts} {counts_2nd}' )

        if  counts < global_threshold:
            class_data = None
            print ( f'Klasse {class_id} - skipping less than {global_threshold} (first)')

        if counts_2nd < global_threshold_2nd:
            class_data_2nd = None
            print (f'Klasse {class_id} - skipping less than {global_threshold_2nd} (second)')
        

    # set meta data 
    if class_data is not None: 
        class_data.class_id     = class_id

    if class_data_2nd is not None: 
        class_data_2nd.class_id = class_id
        

    
    return class_data, class_data_2nd


def print_questions() -> None :
    for qq in zip(list(range(0, len(header))), header):
        print (*qq)

    for qq in zip(list(range(0, len(header_2nd))), header_2nd):
        print (*qq)


def dev_evaluate_classes():

    # use global data_sets
    pass
    

def get_classes() -> list: 



    list_of_classes_1 =  set(votes[header[1]].values)
    list_of_classes_2 =  set(votes_2nd[header_2nd[1]].values)
    
    list_of_classes = list_of_classes_1.union(list_of_classes_2) 
    
    print ('xxx', list_of_classes)

    return sorted(list_of_classes)



def get_classes_of_level(class_level: str) -> list:
    
    assert int(class_level) in range(1,7)
 
    classes_in_level = [class_id for class_id in global_class_list if (class_id[0]) == class_level]

    return classes_in_level


def get_item_list(data            : pd.DataFrame, 
                    second_data_set : bool,
                    question_nr     : int,
    ):

    header_str = header_2nd[question_nr] if second_data_set else header[question_nr]

    item_list = (sorted(set(data[header_str].values)))

    return item_list



def print_item_list(data            : pd.DataFrame, 
                    second_data_set : bool,
                    question_nr     : int,
    ):

    item_list = get_item_list(data, second_data_set, question_nr)
    
    for ii in item_list : print (f"'{ii}',")


def mini_test(data: pd.DataFrame,
              data_2nd: pd.DataFrame=None):

    values     = data[header[1]].value_counts() 
    values_2nd = data_2nd[header_2nd[1]].value_counts()

    print (values, values_2nd)

    pass

    
def answers_per_class(data: pd.DataFrame, title: str ='', 
                      file_format: str = 'pdf', debug: bool = False, data_2nd=None) -> str :


    
#    palette = sns.color_palette( color_order )



    x_order = sorted(set(data[header[1]].values))


    values = data[header[1]].value_counts() 
#    print (values.sort_index())

    values_2 = data_2nd[header_2nd[1]].value_counts()
#    print (values_2.sort_index())

    colors = []
    for ii in values.sort_index().items() :
        #print (*ii)
        if ii[1] < global_threshold :
            colors.append (default_red)
        elif ii[1] < 11 :
            colors.append (default_orange)
        else:
            colors.append (default_green)

    palette = sns.color_palette( colors )


    classes_fig, ax_1, = \
        plt.subplots(1, 1, figsize=(a4_landscape), sharex=True)

    
    colors = ['lawngreen','lawngreen','fuchsia','lawngreen','lawngreen',
                 'lawngreen','lawngreen','lawngreen','lawngreen',
                 'lawngreen','lawngreen','lawngreen','lawngreen',
                 'lawngreen','lawngreen','fuchsia','fuchsia',
                 'lawngreen','fuchsia','lawngreen','fuchsia','fuchsia',
                 'lawngreen','lawngreen','fuchsia','lawngreen',]

    ax_1.scatter(global_class_list,              
                [1,1,0.2,2,4,
                 1,2,1,1,
                 1,2,1,1,
                 1,1,0.2,0.2,
                 1,0.2,1,0.2,0.2,
                 1,1,0.2,1,], c=colors, zorder= 5)





    ax = sns.countplot(x=data[header[1]], data=data, order=x_order,
                       palette=palette)


    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')


    plt.title(title)
   
    ax.set_xlabel('')
    ax.set_ylabel('Anzahl')

    ax.hlines(y=3.2, xmin=-1 , xmax=28, colors=default_red, linestyles='solid', label='', data=None,)
    xxx = ax.text(24.71, 2 , 
                  f"""mind. {global_threshold} Eltern-Antworten 
pro Klasse sind notwendig""",
                  ha="left",
                  size=12,
                  bbox=dict(boxstyle='round',  ec="k", facecolor='wheat', alpha=0.5),
                  wrap=False)

    xxx = ax.text(25.71, 0.6 , 
                  f"""Anz. Antworten \nder Elternsprecher""",
                  ha="left",
                  size=12,
                  bbox=dict(boxstyle='round',  ec="k", facecolor='wheat', alpha=0.5),
                  wrap=False)


    plt.xticks(rotation=270, horizontalalignment="right")



    if debug:
        plt.show()
        
    file_name = generate_file_name(title, data.class_id, file_format) 
    plt.savefig(file_name, dpi=300)

    classes_fig.clf()

    return file_name



def how_do_you_feel (data: pd.DataFrame, title: str ='', 
                         file_format: str = 'pdf', debug:bool=False) -> str :

    
    # TODO: remove refernce to global header

    second_data_set = False
    
    order = [  'sehr gut' , 
               'gut (mit Höhen und Tiefen)', 
               'angespannt', 
               'nicht gut - sehr angespannt'
               ]

    file_name = multi_bar(data, 
                          title, 

                          question_nr_1   = 2, 
                          question_nr_2   = 3, 
 
                          description_1   = 'Schüler:in',
                          description_2   = 'Eltern',
                    
                          order           = order, 

                          second_data_set = False,
                          rotation        = -40,
                          file_format     = file_format,                  
                          debug           = debug,
                          )

    return file_name



def organisation_rating (data: pd.DataFrame, title: str ='', 
                             file_format: str = 'pdf', debug: bool=False) -> str :


    second_data_set = False
                                     
    order= list(range(1, 7))

    color_order= [
        'green',
        'yellowgreen',
        'lightgreen',
        'gold', 
        'red',
        'darkred',
        ]

    file_name = generate_bar_diagram(data, 
                                     question_nr         = 4,
                                     order               = order,
                                     
                                     title               = title, 
                                     color_order         = color_order,

                                     #figsize             : tuple = (a4_landscape),
                                     top                 = 0.75,
                                     bottom              = 0.5,
                                     #rotation            : int   = 0,
                                     #horizontalalignment : str   ="right",
                                     
                                     second_data_set     = second_data_set,
                                     file_format         = file_format, 
                                     debug               = debug,
                                     )
   
    return file_name




def amount_of_work (data: pd.DataFrame, title: str ='', 
                        file_format: str = 'pdf', debug: bool=False) -> str :


    order= [
        'Eher gering', 
        'Genau richtig / angemessen', 
        'Hoch', 
        'Sehr hoch']

    color_order= [
        'green',
        'yellowgreen',
        'orangered', 
        'darkred',
        ]

    file_name = generate_bar_diagram(data, 
                                     question_nr         = 6,
                                     second_data_set     = False,
                                     order               = order,
                                     
                                     title               = title, 
                                     color_order         = color_order,

                                     top                 = 0.75,
                                     bottom              = 0.5,
                                     
                                     file_format         = file_format, 
                                     debug               = debug,
                                     )
   
    return file_name




def work_location (data: pd.DataFrame, title: str ='', 
                   file_format: str = 'pdf', debug: bool=False) -> str :
    """graphics for question 5 
    
    TODO: percentage
    
    """

    order = [            
        'eine Mischform (Zu Hause/ In der Notbetreuung)',
        'In der Schule / In der Notbetreuung',
        'Zu Hause',
        ]

    color_order= [
        default_orange,
        default_red,
#        default_green,
        default_blue,
        ]
    


    file_name = generate_pie(data             = data,
                             second_data_set  = False,                             
                             question_nr      = 5,
                             title            = title,
 
                             order            = order,
                             color_order      = color_order,
                             
                             file_format      = 'pdf',
#                            print_items      = True,
                             debug            = debug, 
                             )

    
    return file_name



def todo_list_in_time(data: pd.DataFrame, title: str ='', 
                      file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
        'nein, die Aufgaben kamen später.' :             default_red,
        'ja, wir konnten die Aufgaben und Materialien ab Sonntag 15:00 ausdrucken.' :      
        default_green,
        })
    
    color_order= [
            ]

    file_name = generate_pie(data            = data, 
                             title           = title, 
                             second_data_set = True,
                             question_nr     = 3,
                                      
                             order            = list(order_dict.keys()),
                             color_order      = list(order_dict.values()),

                             file_format     = file_format, 
#                            print_items      = True,
                             debug           = debug, 

                             )

    return file_name


def amendments (data: pd.DataFrame, 
                title: str ='x', 
                question_nr_1: int = 4, 
                question_nr_2: int = 5, 
                file_format: str = 'pdf',                  
                debug: bool=False) -> str :


    second_data_set = True,
                
    # print_item_list(data, question_nr_1, second_data_set)

    order = ['ja',
             'nein',]

    rotation=-40

    file_name = multi_bar(data, 
                    title, 

                    question_nr_1   = 4, 
                    question_nr_2   = 5, 
 
                    description_1   = 'Hauptfach',
                    description_2   = 'Nebenfach',
                    
                    order           = order, 

                    second_data_set = second_data_set,
                    rotation        = -40,
                    file_format     = file_format,                  
                    debug           = debug,
              )

    return file_name
    

def common_plan(data: pd.DataFrame, title: str ='', question_nr:int = 2, 
               file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
        'Die Aufgaben wurden über verschiedene Kanäle (unübersichtlich) bereitgestellt/verteilt.':
            default_red,

        'Die Aufgaben wurden inhaltlich einheitlich, aber in mehreren Wochenplänen ausgestaltet.':
            default_orange,
             
        'Alle Aufgaben wurden einheitlich in nur einem Wochenplan zusammengeführt.':
            default_green,
            #default_blue,


        'Andere Varianten, bitte in der letzten Frage ausformulieren.' : 
            default_grey, 
        })
        

    file_name = generate_pie(data             = data, 
                             second_data_set  = True,
                             question_nr      = question_nr,

                             title            = title, 
                             
                             order            = list(order_dict.keys()),
                             color_order      = list(order_dict.values()),

                             file_format      = file_format, 
#                            print_items      = True,
                             debug            = debug, 
                             )

    return file_name


def readablity(data: pd.DataFrame, title: str ='', question_nr:int = 6, 
                      file_format: str = 'pdf', debug: bool=False) -> str :

    
    order_dict = OrderedDict({
            'nein, es gab viele unleserlicheDokumente.' : default_red,

            'die meisten Dokumente waren leserlich - jedoch mit Ausnahmen.' : default_orange,

            'ja, alle Dokumente waren gut leserlich.' :  default_green,  #default_blue,
            

        })
        

    file_name = generate_pie(data           = data, 
                             second_data_set= True,
                             question_nr    = question_nr,

                             title          = title, 
                             
                             order          = list(order_dict.keys()),
                             color_order    = list(order_dict.values()),

                             file_format    =file_format, 
                             debug          =debug, 
                             )

    return file_name



def pdf_formated(data: pd.DataFrame, title: str ='',
                      file_format: str = 'pdf', debug: bool=False) -> str :

    order_dict = OrderedDict({
        'nein, es gab auch andere Dateiformate, ohne dass dies notwendig war.': default_red,
        'ja, wir haben alle Dokumente als pdf erhalten.' : default_green,
        })


    file_name = generate_pie(data            = data, 
                             second_data_set = True,
                             question_nr     = 7,
                             title           = title, 
                                                        
                             order          = list(order_dict.keys()),
                             color_order    = list(order_dict.values()),
                             
                             file_format     = file_format, 
                             debug           = debug, 
                             
                             )

    return file_name


def single_point_of_storage(data: pd.DataFrame, title: str ='', question_nr:int = 8, 
                      file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
       'nein, wir mussten uns dieAufgabenblätter aus unterschiedlichenQuellen/Kanälen zusammensuchen.':
           default_blue,


       'Verweis auf Youtubelinks und Musikdateien':
           default_brown,

       'Zunächst per E-Mail, für kommende Woche Abholung im Schulgebäude':
           default_orange,

       'ja, alle Arbeitsmaterialien wurden im IServ/ Padlet bereitgestellt.':
                   default_green, #default_blue,
        })
    
    file_name = generate_pie(data            = data, 
                             second_data_set = True,
                             question_nr     = 8,
                             title           = title, 
                             
                             order          = list(order_dict.keys()),
                             color_order    = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name


def folder_structure(data: pd.DataFrame, title: str ='', 
                      file_format: str = 'pdf', debug: bool=False) -> str :




    order_dict = OrderedDict({
        'nein, es gibt keine Ordnerstruktur.' : default_red,
        'ja, es gibt einen Wochenordner mit Unterordnern für die einzelnen Fächer.': default_green,
#default_blue,
        'nicht relevant (1./2. Klasse)' : default_grey,
        })
    

    file_name = generate_pie(data            = data, 
                             second_data_set = True,
                             question_nr     = 9,
                             title           = title, 
                             
                             order          = list(order_dict.keys()),
                             color_order    = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name


def home_work (data: pd.DataFrame, title: str ='', question_nr:int = 7, 
               file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
        'Trifft nicht zu' : default_orange, 
        'Trifft immer zu' : 'green',
        'Trifft meist zu' : default_green, 
        'Kann ich nicht beurteilen': default_grey, 
        })


    file_name = generate_pie(data            = data, 
                             second_data_set = False,
                             question_nr     = question_nr,
                             title           = title, 
                             
                             order           = list(order_dict.keys()),
                             color_order     = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name


def time_limit (data: pd.DataFrame, title: str ='', 
                file_format: str = 'pdf', debug: bool=False) -> str :
 
    question_nr = 11
    

    color_order= [
#        'lightgreen',
        'yellowgreen',
        'green',
#        'gold', 
        'orangered', 
        'red',
        'darkred',
        ]


    order = [
        'ja, für alle Aufgaben', 
        'ja, für die meisten Aufgaben', 
        'ja, für ein paar Aufgaben', 
        'ja, es wurden nur zusammengefasste Zeitangaben gemacht (bspw. pro Fach oder gesamte Wochenstunden)', 
        'nein, es wurden keine Zeitangaben gemacht']


    # graphic stuff
    figsize=a4_landscape
    top=0.9
    bottom=0.5
    rotation=70
    horizontalalignment="right"


    ret = generate_bar_diagram(data=data, 
                               question_nr=question_nr,
                               title=title, 
                               order=order,
                               color_order=color_order,
                               
                               figsize=figsize,
                               top=top,
                               bottom=bottom,
                               rotation=rotation,
                               horizontalalignment=horizontalalignment,
                         
                               file_format=file_format, 
                               debug=debug
                         
                               )

    return ret



def  working_speed(data: pd.DataFrame, title: str ='', file_format: str = 'pdf', debug: bool=False) -> str :
 
    question_nr = 12

    #item_list = (sorted(set(data[header[question_nr]].values)))
    #print(item_list)
    
    color_order= [
        'lightgreen',
        'yellowgreen',
        'green',
#        'gold', 
        'orangered', 
        'red',
        'darkred',
        ]


    order = [
        '- war immer schneller fertig.', 
        '- war häufig schneller fertig.', 
        '- war meistens innerhalb der vorgegeben Zeit fertig.',
        '- hatte häufig länger gebraucht.', 
        '- brauchte immer länger.',
        '- Keine Bewertung möglich',  
        ]


    # graphic stuff
    figsize=a4_landscape
    top=0.9
    bottom=0.5
    rotation=70
    horizontalalignment="right"


    #item_list = (sorted(set(data[header_str].values)))
    #print(item_list)
    
    ret = generate_bar_diagram(data=data, 
                               question_nr=question_nr,
                               title=title, 
                               order=order,
                               color_order=color_order,

                               figsize=figsize,
                               top=top,
                               bottom=bottom,
                               rotation=rotation,
                               horizontalalignment=horizontalalignment,
                         
                               file_format=file_format, 
                               debug=debug
                         
                               )

    return ret




def support_needed (data: pd.DataFrame, title: str ='', file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
        'keine Unterstützung nötig, eigenständig gelöst' : default_green, 
        'geringe Unterstützung (nicht mehr als bei Hausaufgaben)': 'gold', 
        'viel Unterstützung (deutlich mehr als bei Hausaufgaben)': default_red,
        'keine eigenständige Umsetzung möglich gewesen': 'darkred', 
        
                             })

    file_name = generate_pie(data            = data, 
                             second_data_set = False,
                             question_nr     = 13,
                             title           = title, 
                             
                             order           = list(order_dict.keys()),
                             color_order     = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name

def motivation (data: pd.DataFrame, 
                title: str ='', 
                file_format: str = 'pdf', 
                debug: bool=False) -> str :


    motivation_order= ['Sehr hoch', 'Hoch', 'Mittel', 'Eher gering', 'Gering']


    file_name = multi_bar(data, 
                          title           = title, 
                          question_nr_1   = 14, 
                          question_nr_2   = 15, 
                          
                          description_1   = 'Motivation vor der Bearbeitung',
                          description_2   = 'Motivation nach der Bearbeitung',
                          
                          order           = motivation_order, 
                          file_format     = 'pdf',                  
                          second_data_set = False,
                          
                          rotation        = -40,
                          
                          debug           = False)



    
    return file_name



def introduction_of_new_topics (data: pd.DataFrame, 
                                title: str ='', 
                                file_format: str = 'pdf', debug: bool=False) -> str :

    """graphics for question 16 
    
    TODO: percentage
    
    """

    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 



    question_nr = 16

    order_dict = OrderedDict({
            'durch Fernunterricht per Videokonferenz': default_green,
            'gar nicht' : default_red,
            'mittels Erklärvideos oder Audiodatei' : default_orange,
            'Anderes': default_grey,
             })


    order           = list(order_dict.keys())

    header_str = header[question_nr]
    data_remaster = data[header_str].to_frame()

    data_remaster   = data_remaster.rename(columns={header[question_nr]: 'xxx'})

    mask = ~data_remaster['xxx'].isin(order)
    column_name = 'xxx'
    data_remaster.loc[mask, column_name] = 'Anderes'

    data_remaster   = data_remaster.rename(columns={'xxx' : header[question_nr] })

    data_remaster.class_id = data.class_id

    file_name = generate_pie(data             = data_remaster,
                             second_data_set  = False,
                             question_nr      = question_nr,
                             title            = title, 

                             order           = order,
                             color_order     = list(order_dict.values()),

                             file_format      = file_format, 
                             debug            = debug, 

                             )

    return file_name


def consultation_hours (data: pd.DataFrame, 
                                title: str ='', 
                                file_format: str = 'pdf', debug: bool=False) -> str :


    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 



    question_nr = 17


    order_dict = OrderedDict({
            'Nein'                   : default_red,
            'Ja, per Telefon'        : default_orange,
            'Ja, per Videokonferenz' : default_green,
            'Anderes'                : default_grey
            })
            
    order = list(order_dict.keys())

    header_str = header[question_nr]
    data_remaster = data[header_str].to_frame()

    data_remaster   = data_remaster.rename(columns={header[question_nr]: 'xxx'})

    mask = ~data_remaster['xxx'].isin(order)
    column_name = 'xxx'
    data_remaster.loc[mask, column_name] = 'Anderes'

    data_remaster   = data_remaster.rename(columns={'xxx' : header[question_nr] })

    data_remaster.class_id = data.class_id

    file_name = generate_pie(data            = data_remaster, 
                             second_data_set = False,
                             question_nr     = question_nr,
                             title           = title, 
                             file_format     = file_format, 
                             debug           = debug, 
                             
                             order           = order,
                             color_order     = list(order_dict.values()),

                             )

    return file_name




def video_session (data: pd.DataFrame, title: str ='', file_format: str = 'pdf', debug: bool=False) -> str :


    order_dict = OrderedDict({
        'ja, es wurden mehrere Videokonferenzen durchgeführt.' : 'green', 
        'ja, eine Videokonferenz hat stattgefunden.' : default_green,
        'ja, aber aus technischen Gründen wurde/n diese abgebrochen oder war/en nicht durchführbar.':
            default_orange,
        'nein, es wurde keine angeboten.' : default_red,
        })

    file_name = generate_pie(data             = data, 
                             second_data_set  = False,
                             question_nr      = 18,
                             title            = title, 

                             order           = list(order_dict.keys()),
                             color_order     = list(order_dict.values()),

                             file_format      = file_format, 
                             debug            = debug, 

                             )

    return file_name

def video_session_quality (data: pd.DataFrame, 
                           title: str ='', 
                           file_format: str = 'pdf', 
                           debug: bool=False) -> str :

    second_data_set = False


    # print_item_list(data, question_nr_1, second_data_set)

    order =   ['sehr gut',
               'ok', 
               'nicht so gut',  
               'unerträglich', 
               'Bewertung nicht möglich']


    file_name = multi_bar(data, 
                    title, 

                    question_nr_1   = 19, 
                    question_nr_2   = 20, 
 
                    description_1   = 'Ton',
                    description_2   = 'Video',
                    
                    order           = order, 

                    second_data_set = False,
                    rotation        = -40,
                    file_format     = file_format,                  
                    debug           = debug,
              )

    return file_name



def quality_of_online_teaching (data: pd.DataFrame, 
                                title: str ='', 
                                file_format: str = 'pdf', debug: bool=False) -> str :

    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 


    question_nr = 21


    order_dict = OrderedDict({
            'sehr viel schulischer Inhalt - es wurde nur Unterrichtsstoff vermittelt':
                'green',

            'viel schulischer Inhalt - es wurde vorallem Unterrichtsstoff vermittelt, es gab jedoch auch etwas sozialen Austausch' :
                default_green,

            'geringer schulischer Inhalt - der soziale Austausch stand aber im Vordergrund (es wurden ein paar schulische Fragen gestellt )':
                default_red,
            
            'gar kein schulischer Inhalt - die Schüler:innen konnten sich vorallem sozial austauschen':
                'darkred',
                

            'keine Bewertung möglich / keine Videokonferenz':
                default_grey,
             })

    order           = list(order_dict.keys())


    header_str = header[question_nr]
    data_remaster = data[header_str].to_frame()

    data_remaster   = data_remaster.rename(columns={header[question_nr]: 'xxx'})

    mask = ~data_remaster['xxx'].isin(order)
    column_name = 'xxx'
    data_remaster.loc[mask, column_name] = 'keine Bewertung möglich / keine Videokonferenz'

    data_remaster   = data_remaster.rename(columns={'xxx' : header[question_nr] })

    data_remaster.class_id = data.class_id

    file_name = generate_pie(data            = data_remaster, 
                             second_data_set = False,
                             question_nr     = question_nr,
                             title           = title, 
                             
                             order           = order,
                             color_order     = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name


def more_online_teaching (data: pd.DataFrame, title: str ='', file_format: str = 'pdf', debug: bool=False) -> str :

    order_dict = OrderedDict({
        'ich wünsche mir für mein Kind mehr Unterricht per Videokonferenz' : default_orange, 
        'jetziger Umfang reicht für mein Kind' : default_blue,
        })
    
 
    file_name = generate_pie(data            = data,
                             title           = title, 
                             second_data_set = False,
                             question_nr     = 22,

                             order           = list(order_dict.keys()),
                             color_order     = list(order_dict.values()),

                             file_format = file_format, 
                             debug       = debug, 
                             
                             )

    return file_name




def uptime (data: pd.DataFrame, title: str ='',
            file_format: str = 'pdf', debug: bool=False) -> str :

    second_data_set = False
    
    order = [  'immer verfügbar', 
               'verfügbar, mit Unterbrechung', 
               'schlechte Verfügbarkeit',
               'Bewertung nicht möglich']

    file_name = multi_bar(data, 
                          title, 

                          question_nr_1   = 23, 
                          question_nr_2   = 24, 
 
                          description_1   = 'IServ',
                          description_2   = 'padlet',
                    
                          order           = order, 

                          second_data_set = False,
                          rotation        = -40,
                          file_format     = file_format,                  
                          debug           = debug,
                          )

    return file_name



def latency (data: pd.DataFrame, title: str ='', 
             file_format: str = 'pdf', debug: bool=False) -> str :

    second_data_set = False

    # print_item_list(data, question_nr_1, second_data_set)

    order = ['flüssiges Arbeiten ohne Wartezeiten möglich',
             'Arbeiten mit Wartezeiten möglich', 
             'Aufgrund langer Wartezeiten ist kein zügiges Arbeiten möglich', 
             'Bewertung nicht möglich' ]

    file_name = multi_bar(data, 
                    title, 

                    question_nr_1   = 25, 
                    question_nr_2   = 26, 
 
                    description_1   = 'IServ',
                    description_2   = 'padlet',
                    
                    order           = order, 

                    second_data_set = False,
                    rotation        = -40,
                    file_format     = file_format,                  
                    debug           = debug,
              )


    return file_name




def frequency (data: pd.DataFrame, title: str ='', file_format: str = 'pdf', debug: bool=False) -> str :

    question_nr = 29

    order_dict = OrderedDict({
        'alle 14 Tage' :default_blue, 
        'wöchentlich'  :default_orange
        })
    

    file_name = generate_pie(data            = data,
                             second_data_set = False,
                             question_nr     = question_nr,
                             title           = title, 

                             order           = list(order_dict.keys()),
                             color_order     = list(order_dict.values()),

                             file_format     = file_format, 
                             debug           = debug, 
                             )

    return file_name





def generate_pie(data             : pd.DataFrame,
                 second_data_set  : bool,

                 question_nr      : int,
                 title            : str ='', 
                 order            : list =[],
                 color_order      : list =[],

                 figsize          : tuple = a4_landscape,
                 print_legend     : bool =True, 

                 file_format      : str = 'pdf',
                 print_items      : bool=False,
                 debug            : bool=False, 

                 
                 
                 ) -> str :


    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 

    if print_items:
        print_item_list(data, second_data_set,  question_nr)

    if second_data_set:
        header_str = header_2nd[question_nr]
    else:
        header_str = header[question_nr]

    if title == '': title = header_str 

    if order is None or len(order) == 0:
        order = get_item_list(data, second_data_set,  question_nr)
    
    if len(color_order) == 0:
        color_order = None

    rating = data[header_str].to_frame()

    rating_fig, ax_1, = \
        plt.subplots(1, 1, figsize=(a4_landscape), sharex=True)

    data_dict = {}

    # sorting values
    for item in order: 
        bla= rating.loc[rating[header_str] == item]
        data_dict.update({item : len(bla)})

    df = pd.DataFrame({'where': list(data_dict.values()),},
                      index=list(data_dict.keys()))


    ax = df.plot.pie(y='where',autopct='%.f', figsize=figsize, ax=ax_1, 
                     colors = color_order )

    plt.title(plot_title(data.class_id, title))  
    ax.set_ylabel('')
    plt.legend(bbox_to_anchor=(1,0),)

    if not print_legend:
        ax.get_legend().remove()

    file_name = generate_file_name(title, data.class_id, file_format) 
    plt.savefig(file_name, dpi=300)
    

    if debug:
        plt.show()

    plt.close(rating_fig) # rating_fig.clf()
    plt.close() 
 
    return file_name



def generate_bar_diagram(data                : pd.DataFrame, 
                         question_nr         : int,
                         order               : list,
                         
                         title               : str    ='', 
#                        color               : str    ='seagreen',
                         color_order         : list   = [],

                         figsize             : tuple = (a4_landscape),
                         top                 : float = 0.75,
                         bottom              : float = 0.5,
                         rotation            : int   = 0,
                         horizontalalignment : str   ="right",
                         
                         second_data_set     : bool = False, 
                         file_format         : str   = 'pdf', 
                         debug               : bool  =False,

                         ) -> str :

    ##################################################################

    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 

    header_str = header_2nd[question_nr] if second_data_set else  header[question_nr]

    if title == '':
        title = header_str 

    rating = data[header_str].to_frame()
    rating = rating.rename(columns={header_str: title})

    palette = sns.color_palette( color_order )
    

    rating_fig, ax_1, = \
        plt.subplots(1, 1, figsize=(a4_landscape), sharex=True)


    rating_fig, ax_1, = \
        plt.subplots(1, 1, figsize=figsize, sharex=True)

    ax = sns.countplot(x=rating[title],
                       order=order, 
#                       color=color,
                       palette=palette,
                       data=rating)

    plt.title(plot_title(data.class_id, title))  
    ax.set_xlabel('')
    ax.set_ylabel('Anzahl')

    sub = plt.subplots_adjust(left=None, bottom=bottom, right=None, top=top, wspace=None, hspace=None)
    plt.xticks(rotation=rotation, horizontalalignment=horizontalalignment)
    

    file_name = generate_file_name(title, data.class_id, file_format) 
    plt.savefig(file_name, dpi=300)
    

    if debug:
        plt.show()

    plt.close(sub) 
#    plt.close(ax) 
    plt.close(rating_fig) # rating_fig.clf()
    plt.close() 
    


    return file_name



def multi_bar(data: pd.DataFrame, 
              title: str , 
              question_nr_1: int, 
              question_nr_2: int, 

              description_1    : str = 'xxxxx',
              description_2    : str = 'yyyyy',

              order            : list = None, 
              file_format      : str = 'pdf',                  
              second_data_set  : bool=True,

              rotation         : int = -40,

              debug: bool=False) -> str :


    if data is None:   # not enough entities for processing on class level 
        return 

    if data.empty:   # skip empty datasets
        return 


    if second_data_set:
        header_str_1 = header_2nd[question_nr_1]
        header_str_2 = header_2nd[question_nr_2]
    else:
        header_str_1 = header[question_nr_1]
        header_str_2 = header[question_nr_2]

    if title == '':
        title = header_str_1 

    data_col_1 = data[header_str_1].to_frame()
    data_col_1 = data_col_1.rename(columns={header_str_1: title})

    data_col_2 = data[header_str_2].to_frame()
    data_col_2 = data_col_2.rename(columns={header_str_2: title})
   

    data_col_1 = data_col_1.assign(extra=lambda x: description_1)
    data_col_2 = data_col_2.assign(extra=lambda x: description_2)

    data_col = pd.concat([data_col_1, data_col_2], ignore_index=True )

    data_col_fig, ax_1, = \
        plt.subplots(1, 1, figsize=(a4_landscape), sharex=True)


    ax = sns.countplot(x=data_col[title],
                       hue=data_col['extra'],
                       order=order, 
                       data=data_col)

    plt.title(plot_title(data.class_id, title))  
    ax.set_xlabel('')
    ax.set_ylabel('Anzahl')

    ax.legend().set_title('')
    plt.legend(bbox_to_anchor=(1,1), loc=1, borderaxespad=-4.)

    plt.xticks(rotation=rotation, horizontalalignment="left")
    plt.subplots_adjust(left=None, bottom=0.5, right=None, top=0.8, wspace=None, hspace=None)
    

    file_name = generate_file_name(title, data.class_id, file_format) 
    plt.savefig(file_name, dpi=300)
    

    if debug:
        plt.show()

    data_col_fig.clf()
    plt.close() 
 
    return file_name






def write_comments_to_file(data, comment_row_nr, file_name, is_second_data_set=False): 

    if is_second_data_set:

        comment_data = data[header_2nd[comment_row_nr]].to_frame()

    else:
        comment_data = data[header[comment_row_nr]].to_frame()


    df = comment_data.dropna()

    with open(file_name, 'w') as file_to_write:
        for index, row in df.iterrows():
            comment = row.values[0]
            file_to_write.write(comment)
            file_to_write.write('\n\n')
        



def get_new_offset(y_offset_old, n_lines):

        line_height = 0.0157
        frame_extra = 0.030
        v_space     = 0.00 #7

        y_offset_new =y_offset_old - (n_lines -1 ) * line_height - frame_extra - v_space 
        
        return y_offset_new



def generate_comment_page(data             : pd.DataFrame,
                          data_2nd         : pd.DataFrame,

                 question_nr      : int,
                 question_nr_2nd  : int,
                 title            : str ='', 
            
  #               figsize          : tuple = a4_landscape,
  #               print_legend     : bool =True, 

                 file_format      : str = 'pdf',
  #               debug            : bool=False, 

                 
                 
                 ) -> str :

    
    header_str = header[question_nr]
    header_str_2nd = header_2nd[question_nr_2nd]
        

    if title == '': title = header_str 

    #remove nan
    
    ans_data = data[header_str]
    ans_data.dropna(inplace=True)

    ans2_data = data_2nd[header_str_2nd]
    ans2_data.dropna(inplace=True)

    xxx = ans_data.append(ans2_data, ignore_index=True)
    ans_data= xxx

    comment_page = plt.figure(figsize=a4_portrait)
    fontsize = 10

    sub_page_nr = 0

    y_offset = 1

    file_names = []

    for ii, comment in enumerate(ans_data): #[textstr, textstr[20:140], textstr[220:], textstr[220: 400]]:
        
        textstr_new= break_long_title(comment, 100).strip()
        n_lines = len(textstr_new.splitlines())
        
        if ii in [52, 58] :
            col = 'red'
            continue
        else: 
            col = 'wheat'
                

        y_offset = get_new_offset (y_offset, n_lines)
        
        if ii == 0 :
            textstr_new = textstr_new.replace('Schuldt', 'XXX')
    
        if ii == 33 :
            textstr_new = textstr_new.replace('Maiwald', 'XXX')
    
        if ii == 96 :
            textstr_new = textstr_new.replace('Wilke', 'XXX')
    

        if y_offset < 0.025 or ii == len(ans_data) -1:
            sub_page_nr += 1
            file_names += [generate_file_name(title, data.class_id, file_format, sub_page_nr) ]
#            print ('###############################',file_names [-1], sub_page_nr, ii, len(ans_data))
            plt.savefig(file_names[-1], dpi=300)
            plt.clf()
            y_offset = 1
            y_offset = get_new_offset (y_offset, n_lines)
            

#        print (n_lines, y_offset, comment)
        xxx = comment_page.text(0.05, y_offset , 
                                textstr_new,
                                ha="left",
                                size=fontsize,
                                bbox=dict(boxstyle='round',  ec="k", facecolor=col, alpha=0.5),
                                wrap=False)

    plt.close(comment_page) 

    return file_names



#def test_output_class_analysis(class_id: str = all) -> None :
#
#    data, data_2nd = load_data_general(class_id)
#    file_format    ='pdf'
#    file_list      = []
#
#    all_classes = True if class_id == 'all' else False
#    
#
#    # Q14 & Q15
#    title='Lernmotivation'
#    file_list += [motivation(data=data, title=title, file_format=file_format )]





def output_class_analysis(class_id: str = all) -> None :

    print(f'\nKlasse {class_id} - processing')
    data, data_2nd = load_data_general(class_id)

    
    file_format='pdf'
    file_list  =[]

    all_classes = True if class_id == 'all' else False
    class_level = True if len(class_id) == 1 else False
    
    # Q1
    if all_classes:
        title = 'Antworten nach Klassen'
        file_list += [answers_per_class(data, title, file_format=file_format, debug=False,data_2nd = data_2nd)]

    # Q2 & Q3
    title = 'Wie erging es Ihnen diese Woche im Homeschooling / in der Notbetreuung?'
    file_list += [how_do_you_feel(data, title=title, file_format=file_format )]

    # Q4
    title='Allgemeine Zufriedenheit mit der Organisation und Umsetzung des Fernunterrichts/Homeschoolings'
    file_list += [organisation_rating (data=data, title=title, file_format=file_format, debug=False)]

    # Q5
    title='Wo wurden die Aufgaben bearbeitet?'
    file_list += [work_location(data=data, title=title, file_format=file_format, debug=False)]

    # QQ 3+4 Wurden die Aufgaben rechtzeitig übermittelt?   
    file_list += [todo_list_in_time(data=data_2nd)]

    file_list += [amendments(data=data_2nd, title='Gab es Nachreichungen von Aufgaben oder nachträgliche Änderungen am Wochenplan?')]

    # QQ 2 Wurde ein einheitlicher Wochenplan bereitgestellt?
    file_list += [common_plan(data=data_2nd )]


    # QQ 6 Wurden die Aufgaben lesbar übermittelt?   
    file_list += [readablity(data=data_2nd)]

    # QQ 7
    file_list += [pdf_formated(data=data_2nd)]

    # QQ 8 Wurden die Arbeitsmaterialien in IServ/ Padlet gesammelt?
    file_list += [single_point_of_storage(data=data_2nd)]

    # QQ 9
    file_list += [folder_structure(data=data_2nd)]


    # Q6
    title='Umfang der Aufgaben'
    file_list += [amount_of_work(data=data, title=title, file_format=file_format, debug=False )]


    #Q  7 Aufgabeninhalt [Die Lernziele waren klar definiert.]
    file_list += [home_work(data=data, question_nr = 7,
                             file_format=file_format, debug=False )]

    #Q  8 Aufgabeninhalt [Die Inhalte waren strukturiert und sorgfältig geplant. ]
    file_list += [home_work(data=data, question_nr = 8,
                             file_format=file_format, debug=False )]

    #Q  9 Aufgabeninhalt [Die Aufgabenstellungen waren klar definiert.]
    file_list += [home_work(data=data, question_nr = 9,
                             file_format=file_format, debug=False )]

    #Q 10 Aufgabeninhalt [Für die Lösung der Aufgaben/ der Lerninhalte waren alle Hilfsmittel/ Quellen verfügbar.]
    file_list += [home_work(data=data, question_nr = 10,
                             file_format=file_format, debug=False )]



    # Q11
    title='Wurden Bearbeitungszeiten zur Aufgabenstellung mit angegeben?'
    file_list += [time_limit(data=data , title=title)]

    # Q12       - Konnte die vorgegebene Zeit zur Bearbeitung der Aufgaben eingehalten werden?
    file_list += [working_speed(data=data)]
    
    # Q13       - Unterstützungsbedarf 
    file_list += [support_needed(data=data)]

    # Q14 & Q15 - Lernmotivation 
    title='Lernmotivation'
    file_list += [motivation(data=data, title=title, file_format=file_format )]

    # Q 16      - Wie wurde die Einführung neuer Themen digital unterstützt?
    file_list += [introduction_of_new_topics (data=data, file_format=file_format )]

    # Q 17      - Wurde eine Lehrersprechstunde angeboten (Klärung von Schülerfragen)?
    file_list += [consultation_hours(data=data)]

    # Q 18      - Wurde in Ihrer Klasse eine Videokonferenz angeboten? 
    file_list += [video_session(data=data)]

    # Q19 & Q20 - Wie war die technische Qualität der Videokonferenz(-en)?
    title='Wie war die technische Qualität der Videokonferenz(-en)?'
    file_list += [video_session_quality(data=data, title=title, 
                                        file_format=file_format, debug=False )]

    # Q 21      - Anteil des schulischen Inhalts in Videokonferenzen 
    file_list += [quality_of_online_teaching(data=data)]

    # Q 22      - Wünschen Sie sich mehr Fernunterricht (=schulische Inhalte) per Videokonferenz? 
    file_list += [more_online_teaching(data=data)]

    if all_classes:
        # Q23 & Q24
        title='Verfügbarkeit von IServ & Padlet (in den Kernzeiten)'
        file_list += [uptime(data=data, title=title, file_format=file_format, debug=False )]
    
        # Q25 & Q26
        title='Latenz/Trägheit von IServ & Padlet (in den Kernzeiten)'
        file_list += [latency(data=data, title=title, file_format=file_format, debug=False )]

        # Q29 Wie oft soll diese Umfrage wiederholt werden?
        file_list += [frequency(data=data)]

        # Comments
        file_list += generate_comment_page(
            data             = data,
            data_2nd         = data_2nd,
            question_nr      = 28,
            question_nr_2nd  = 10,
            file_format      = 'pdf',
                             )



    ######### 2nd  ######

    file_list = [ff for ff in file_list if ff is not None]

    if all_classes:
        result_file_name = "Zusammenfassung_alle_Klassen.pdf"
    elif class_level:
        
        result_file_name = f"Zusammenfassung_Klassenstufe_{class_id}.pdf"
    else:
        result_file_name = f"Zusammenfassung_Klasse_{class_id}.pdf"


    if len(file_list) == 0:
        return []
    
    # annoying bug
    xxx = file_list + [ result_file_name ] 
    return xxx

    


def merge_pdfs(file_list, result_file_name):
    
    if len(file_list) == 0: # skip empty lists
        return

    from PyPDF2 import PdfFileMerger
    
    merger = PdfFileMerger()

    for pdf in file_list:
        if pdf is None: continue
        merger.append(pdf)
        
    merger.write(result_file_name)
    merger.close()



def process_all_pdf():  # annoying unfixed bug in pyPDF2 overwriting python's standart warnings

    data, data_2nd = load_data_general()


    list_of_lists = []

    list_of_classes = global_class_list + ['all'] #+  ['1', '2', '3', '4', '5', '6',] 

    for class_id in list_of_classes: 
        list_of_lists += [output_class_analysis(class_id)]

    for class_files_list in list_of_lists:
        if len(class_files_list) == 0: # skip empty lists
            continue
        result_file_name = class_files_list.pop(-1)
        
        merge_pdfs(file_list=class_files_list, result_file_name=result_file_name)


def process_pdf_selected():  # annoying unfixed bug in pyPDF2 overwriting python's standart warnings


    data, data_2nd = load_data_general()

#    print( enought_answers_for_this_class(data, class_id = '2c'))

    list_of_lists = []

    list_of_lists += [output_class_analysis(class_id='all')]
#    list_of_lists += [output_class_analysis(class_id='1c')]
#    list_of_lists += [output_class_analysis(class_id='4b')]

    

    for result in list_of_lists:
        result_file_name = result.pop(-1)
        merge_pdfs(file_list=result, result_file_name=result_file_name)

        



def devel():

#   my_2c_data = load_data(class_id='2c')
    
    data, data_2nd = load_data_general()

    mini_test(data, data_2nd)


def xxx():
#    write_comments_to_file(data, comment_row_nr = 28, file_name = 'Kommentare_Elternumfrage.txt')
#    write_comments_to_file(data_2nd, comment_row_nr = 10, file_name = 'Kommentare_Distanzlernen.txt', is_second_data_set=True)

#    print (data)
#    print (data_2nd)

#    print_questions()

    order=[]
    color_order=[]

    file_names = generate_comment_page(
        data             = data,
        data_2nd         = data_2nd,
        question_nr      = 28,
        question_nr_2nd  = 10,
 #       title            = title,
 
        file_format      = 'pdf',
        #print_items      = True,
#        debug            = debug, 
                             )
    merge_pdfs(file_names, 'Comments.pdf')



if __name__ == '__main__' :
    

    devel()
#     process_pdf_selected()
    
#    process_all_pdf()



#######################

# TODO: make sure that all classes are set in both data sets have the same 
# TODO: dont evaluate classes with too litle data
# TODO: make sure that colors fit green - good  amber - ok  red - bad but only item in goot and bad
