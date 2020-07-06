import pandas as pd
import numpy as np
import networkx as nx
from bokeh.models import Range1d, Plot, ResetTool, PanTool, ColumnDataSource, LabelSet, TapTool, BoxZoomTool
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.models import Circle, MultiLine
from bokeh.plotting import from_networkx, curdoc
from bokeh.io import show, output_notebook, reset_output, output_file
from bokeh.layouts import column

def convert_StringList2ListOfInt(string2convert):
    if string2convert == '[]':
        return []
    else:
        return [int(ele) for ele in string2convert[1:-1].split(',')]

def DataFrame_StringOfInts2ListOfInts(df, cols2convert_list):
    for column in cols2convert_list:
        column_temp = column + "_temp"
        df[column_temp] = df[column].apply(convert_StringList2ListOfInt, 1)
        df[column] = df[column_temp]
        df = df.drop(column_temp, axis=1)
    return df

#path = r'D:/Documents/DataScience/Portfolio/criticalrole_webscraper_knowledgegraph/'
result_df = pd.read_csv('../critrole_w2v_model_output.csv')
result_df = DataFrame_StringOfInts2ListOfInts(result_df, ['word_most_similar_indices'])
#result_df['word_most_similar_indices'] = result_df['word_most_similar_indices'].apply(ast.literal_eval)
result_df['coords'] = list(zip(result_df['dim0'], result_df['dim1']))

result_pos = result_df['coords'].to_dict()
result_links = result_df['word_most_similar_indices'].to_dict()
result_cds = ColumnDataSource(result_df)
G = nx.from_dict_of_lists(result_links)

reset_output()
#output_notebook()
#output_file('critrole_w2v_visualizer.html')

# We could use figure here but don't want all the axes and titles
plot = Plot(x_range=Range1d(-2, 2), y_range=Range1d(-2, 2))

# Create a Bokeh graph from the NetworkX input using nx.spring_layout
#nx.set_node_attributes(G, result_pos, 'coord')
graph = from_networkx(G, layout_function = result_pos)

graph.node_renderer.glyph = Circle(size=4, fill_color='#2b83ba', line_width=0)
graph.edge_renderer.glyph = MultiLine(line_color="#cccccc", line_alpha=0.8, line_width=0)

graph.node_renderer.selection_glyph  = Circle(size=4, fill_color='red', line_alpha=0.8, line_width=1)
graph.edge_renderer.selection_glyph  = MultiLine(line_color='red', line_alpha=0.8, line_width=3)
plot.renderers.append(graph)

result_cds = ColumnDataSource(pd.DataFrame({'dim0': result_df.loc[:,'dim0'], 'dim1': result_df.loc[:,'dim1'], 'word': result_df['word']}))
labels = LabelSet(x='dim0', y='dim1', text='word',
                  level='glyph', x_offset=0, y_offset=0, source=result_cds, render_mode='canvas',
                  text_font_size="11px", text_font='calibri', text_alpha=1)
plot.renderers.append(labels)

#graph.node_renderer.data_source.data['labels'] = result_df['word']
#node_renderer.glyph.update
graph.selection_policy = NodesAndLinkedEdges()
plot.add_tools(TapTool(), BoxZoomTool(), PanTool(), ResetTool())

#show(plot)
curdoc().add_root(column(plot))