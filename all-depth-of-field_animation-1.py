# 导入 manim 库中的所有类
from manim import *
# 导入 numpy 库用于数学计算
import numpy as np

# 设置全局背景色为深色
config.background_color = "#1C1C1C"

# 定义场景类，继承自 Scene
class DOFScene(Scene):
    # 辅助函数：创建工程图纸风格的垂直尺寸标注（适用于 l 和 Delta）
    def create_vertical_dimension(self, p1, p2, text, offset=1.0, color=WHITE):
        # 计算两个点之间的水平向量
        vec = p2 - p1
        # 归一化向量
        unit_vec = vec / np.linalg.norm(vec)
        # 计算向下的垂直向量
        perp_vec = np.array([0, -1, 0])
        # 计算尺寸线端点1的坐标（向下偏移）
        ext_p1 = p1 + perp_vec * offset
        # 计算尺寸线端点2的坐标（向下偏移）
        ext_p2 = p2 + perp_vec * offset
        # 绘制从原点到尺寸线端点的细引线（向下延长一点）
        line_ext1 = Line(p1, ext_p1 + perp_vec * 0.2, color=color, stroke_width=1)
        # 绘制从另一个原点到尺寸线端点的细引线（向下延长一点）
        line_ext2 = Line(p2, ext_p2 + perp_vec * 0.2, color=color, stroke_width=1)
        # 绘制尺寸线主体（连接两个偏移端点）
        dim_line = Line(ext_p1, ext_p2, color=color, stroke_width=2)
        # 在尺寸线左端添加朝内的箭头（指向左端点）
        arrow1 = Arrow(ext_p1 + unit_vec * 0.4, ext_p1, buff=0, color=color, tip_length=0.15)
        # 在尺寸线右端添加朝内的箭头（指向右端点）
        arrow2 = Arrow(ext_p2 - unit_vec * 0.4, ext_p2, buff=0, color=color, tip_length=0.15)
        # 计算尺寸线的中点
        mid_point = (ext_p1 + ext_p2) / 2
        # 计算尺寸文字的位置（再向下偏移一点，避免压线）
        text_pos = mid_point + perp_vec * 0.3
        # 创建尺寸文字的数学文本对象
        text_mobj = MathTex(text, font_size=32, color=color).move_to(text_pos)
        # 返回包含所有尺寸标注元素的组
        return VGroup(line_ext1, line_ext2, dim_line, arrow1, arrow2, text_mobj)

    # 辅助函数：创建工程图纸风格的斜向尺寸标注（适用于 z 和 z'）
    def create_slanted_dimension(self, p1, p2, text, direction=UL, offset=0.8, color=WHITE):
        # 判断方向（使用 np.array_equal 避免数组比较报错）
        if np.array_equal(direction, UL):
            # 左上方向向量
            unit_vec = np.array([-1, 1, 0]) / np.sqrt(2)
        # 如果是右下角
        elif np.array_equal(direction, DR):
            # 右下方向向量
            unit_vec = np.array([1, -1, 0]) / np.sqrt(2)
        # 默认左上角
        else:
            # 默认左上方向向量
            unit_vec = np.array([-1, 1, 0]) / np.sqrt(2)
        # 计算尺寸线端点的坐标（沿着斜向单位向量偏移）
        ext_p1 = p1 + unit_vec * offset
        # 计算另一个尺寸线端点
        ext_p2 = p2 + unit_vec * offset
        # 绘制从原点到尺寸线端点的细引线，稍微延长一点
        line_ext1 = Line(p1, ext_p1 + unit_vec * 0.15, color=color, stroke_width=1)
        # 绘制从另一个原点到尺寸线端点的细引线
        line_ext2 = Line(p2, ext_p2 + unit_vec * 0.15, color=color, stroke_width=1)
        # 绘制尺寸线主体（连接两个偏移端点）
        dim_line = Line(ext_p1, ext_p2, color=color, stroke_width=2)
        # 确定尺寸线的方向向量（用于箭头方向）
        line_vec = ext_p2 - ext_p1
        # 归一化尺寸线方向向量
        line_unit_vec = line_vec / np.linalg.norm(line_vec)
        # 在尺寸线左端添加朝内的箭头
        arrow1 = Arrow(ext_p1 + line_unit_vec * 0.4, ext_p1, buff=0, color=color, tip_length=0.15)
        # 在尺寸线右端添加朝内的箭头
        arrow2 = Arrow(ext_p2 - line_unit_vec * 0.4, ext_p2, buff=0, color=color, tip_length=0.15)
        # 计算尺寸线的中点坐标
        mid_point = (ext_p1 + ext_p2) / 2
        # 计算尺寸文字的位置（偏移一点，避免与尺寸线交叠）
        text_pos = mid_point + unit_vec * 0.2
        # 创建尺寸文字的数学文本对象
        text_mobj = MathTex(text, font_size=32, color=color).move_to(text_pos)
        # 返回包含所有尺寸标注元素的组
        return VGroup(line_ext1, line_ext2, dim_line, arrow1, arrow2, text_mobj)

    # 辅助函数：创建带中间箭头的实线/虚线光线
    def create_ray_with_mid_arrow(self, start, end, color, is_dashed=False):
        # 判断是否使用虚线
        if is_dashed:
            # 创建虚线
            line = DashedLine(start, end, color=color, stroke_width=2)
        # 如果不是虚线（即实线）
        else:
            # 创建实线
            line = Line(start, end, color=color, stroke_width=2)
        # 获取线的中点
        mid_point = line.get_center()
        # 获取线的角度
        angle = line.get_angle()
        # 创建短箭头，初始放置在线上
        arrow = Arrow(start=mid_point - RIGHT*0.2, end=mid_point + RIGHT*0.2, buff=0, color=color, tip_length=0.12, stroke_width=2)
        # 旋转箭头与线对齐
        arrow.rotate(angle, about_point=mid_point)
        # 返回包含线和箭头的组
        return VGroup(line, arrow)

    # 主构建方法，Manim 动画的入口
    def construct(self):
        # =====================================================================
        # ==================== 远景深度演示（第一部分） =======================
        # =====================================================================
        
        # 设定入瞳半口径（用于确定入瞳高度）
        a_val = 1.0
        # 设定远景物距 l
        l_val = 2.5
        # 设定远景深度 delta
        delta_val = 1.0
        # 设定整体向右平移的量（用于腾出右侧空间）
        shift_x = 1.5
        
        # 计算远景平面 X 坐标
        x_far = -l_val - delta_val - shift_x
        # 计算远景对焦平面 X 坐标
        x_focus = -l_val - shift_x
        # 计算远景入瞳面 X 坐标
        x_pupil = -shift_x  
        # 计算远景像面 X 坐标
        x_image = 2.0 - shift_x
        
        # 【远景标题】创建远景标题文字
        title_far = Text("一、远景深度计算", font="SimHei", font_size=72, color=WHITE)
        # 将远景标题移动到屏幕正中央
        title_far.move_to(ORIGIN)
        # 播放远景标题淡入动画
        self.play(FadeIn(title_far))
        # 停留 1.5 秒供观众看清
        self.wait(1.5)
        # 播放远景标题淡出动画
        self.play(FadeOut(title_far))

        # 创建远景光轴线段
        optical_axis = Line(start=LEFT * 6.5, end=RIGHT * 1.0, color=WHITE)
        # 创建远景对焦平面线段
        focus_plane = Line(start=np.array([x_focus, -2.2, 0]), end=np.array([x_focus, 2.2, 0]), color=GREEN)
        # 创建远景入瞳面线段
        pupil_line = Line(start=np.array([x_pupil, -a_val, 0]), end=np.array([x_pupil, a_val, 0]), color=YELLOW)
        # 创建远景像面线段
        image_plane = Line(start=np.array([x_image, -1.1, 0]), end=np.array([x_image, 1.1, 0]), color=BLUE)
        
        # 创建远景光轴标签文字
        label_axis = Text("光轴", font="SimHei", font_size=24).move_to(np.array([-6.0, -0.4, 0]))
        # 创建远景入瞳标签文字
        label_pupil = Text("入瞳", font="SimHei", font_size=24, color=YELLOW).next_to(pupil_line, UP, buff=0.3)
        # 创建远景对焦平面标签文字
        label_focus = Text("对焦平面", font="SimHei", font_size=24, color=GREEN).next_to(focus_plane, UP, buff=0.1)
        # 创建远景像面标签文字
        label_image = Text("像面(探测器)", font="SimHei", font_size=24, color=BLUE).next_to(image_plane, UP, buff=0.1)
        
        # 播放远景基础几何线段创建动画
        self.play(Create(optical_axis), Create(focus_plane), Create(pupil_line), Create(image_plane))
        # 播放远景基础标签文字淡入动画
        self.play(FadeIn(label_axis), FadeIn(label_pupil), FadeIn(label_focus), FadeIn(label_image))
        
        # 创建远景平面虚线
        far_plane = DashedLine(start=np.array([x_far, -1.6, 0]), end=np.array([x_far, 1.6, 0]), color=PURPLE)
        # 创建远景平面标签文字
        label_far = Text("远景平面", font="SimHei", font_size=20, color=PURPLE).next_to(far_plane, UP, buff=0.1)
        # 播放远景平面创建动画
        self.play(Create(far_plane), FadeIn(label_far))
        
        # 创建远景物距 l 的垂直尺寸标注
        dim_l = self.create_vertical_dimension(np.array([x_focus, 0, 0]), np.array([x_pupil, 0, 0]), "l", offset=2.0, color=WHITE)  
        # 创建远景深度 Delta_1 的垂直尺寸标注
        dim_delta = self.create_vertical_dimension(np.array([x_far, 0, 0]), np.array([x_focus, 0, 0]), r"\Delta_1", offset=1.6, color=WHITE)
        # 播放远景尺寸标注创建动画
        self.play(Create(dim_l), Create(dim_delta))
        # 等待 2 秒
        self.wait(2)

        # 计算远景 A 点（对焦平面与光轴交点）的坐标
        point_A = np.array([x_focus, 0, 0])
        # 计算远景入瞳上边缘点坐标
        point_a_top = np.array([x_pupil, a_val, 0])
        # 计算远景入瞳下边缘点坐标
        point_a_bot = np.array([x_pupil, -a_val, 0])
        # 计算远景像面中心点坐标
        point_image_center = np.array([x_image, 0, 0])
        
        # 创建远景 A 点圆点
        dot_A = Dot(point_A, color=RED_E, radius=0.05)
        # 创建远景 A 点标签文字
        label_A = MathTex("A", font_size=24, color=RED_E).next_to(dot_A, DOWN, buff=0.2).shift(LEFT*0.2)
        # 播放远景 A 点及其标签动画
        self.play(FadeIn(dot_A), FadeIn(label_A))
        
        # 创建从远景 A 到入瞳上边缘的光线
        ray1_A_to_top = self.create_ray_with_mid_arrow(point_A, point_a_top, BLUE_B)
        # 创建从远景 A 到入瞳下边缘的光线
        ray2_A_to_bot = self.create_ray_with_mid_arrow(point_A, point_a_bot, BLUE_B)
        # 播放远景发散光线创建动画
        self.play(Create(ray1_A_to_top), Create(ray2_A_to_bot))
        # 等待 0.5 秒
        self.wait(0.5)
        
        # 创建从远景入瞳上边缘到像面中心的光线
        ray1_top_to_img = self.create_ray_with_mid_arrow(point_a_top, point_image_center, BLUE_B)
        # 创建从远景入瞳下边缘到像面中心的光线
        ray2_bot_to_img = self.create_ray_with_mid_arrow(point_a_bot, point_image_center, BLUE_B)
        # 播放远景汇聚光线创建动画
        self.play(Create(ray1_top_to_img), Create(ray2_bot_to_img))
        # 等待 2 秒
        self.wait(2)
        
        # 创建远景 A 点光路说明文字
        text_part1 = Text("A点发出充满入瞳口径的上下光线，先发散，后汇聚在像面中心", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景说明文字淡入
        self.play(FadeIn(text_part1))
        # 等待 2 秒
        self.wait(2)
        # 播放远景说明文字淡出
        self.play(FadeOut(text_part1))

        # 计算远景 B 点（远景平面与光轴交点）的坐标
        point_B = np.array([x_far, 0, 0])
        # 创建远景 B 点圆点
        dot_B = Dot(point_B, color=YELLOW)
        # 创建远景 B 点标签文字
        label_B = MathTex("B", font_size=20, color=YELLOW).next_to(dot_B, DOWN, buff=0.2).shift(LEFT*0.2)
        # 播放远景 B 点及其标签动画
        self.play(FadeIn(dot_B), FadeIn(label_B))
        
        # 计算远景光线 3（B 到 a_top）的斜率
        slope_3 = (a_val - 0) / (x_pupil - x_far)
        # 计算远景光线 3 与对焦平面的交点 y 坐标
        y_z1 = slope_3 * (x_focus - x_far)
        # 计算远景交点 z1 的坐标
        point_z1 = np.array([x_focus, y_z1, 0])
        
        # 计算远景光线 4（B 到 a_bot）的斜率
        slope_4 = (-a_val - 0) / (x_pupil - x_far)
        # 计算远景光线 4 与对焦平面的交点 y 坐标
        y_z2 = slope_4 * (x_focus - x_far)
        # 计算远景交点 z2 的坐标
        point_z2 = np.array([x_focus, y_z2, 0])
        
        # 创建从远景 B 到入瞳上边缘的虚线光线
        ray3_B_to_top = self.create_ray_with_mid_arrow(point_B, point_a_top, GREEN_B, is_dashed=True)
        # 创建从远景 B 到入瞳下边缘的虚线光线
        ray4_B_to_bot = self.create_ray_with_mid_arrow(point_B, point_a_bot, GREEN_B, is_dashed=True)
        
        # 创建远景 z1 点圆点
        dot_z1 = Dot(point_z1, color=DARK_BLUE, radius=0.06)
        # 创建远景 z2 点圆点
        dot_z2 = Dot(point_z2, color=DARK_BLUE, radius=0.06)
        # 创建远景 z1 点标签文字
        label_z1 = MathTex("z_1", font_size=30, color=WHITE).next_to(dot_z1, UP, buff=0.20).shift(RIGHT*0.3)
        # 创建远景 z2 点标签文字
        label_z2 = MathTex("z_2", font_size=30, color=WHITE).next_to(dot_z2, DOWN, buff=0.20).shift(RIGHT*0.3)
        
        # 播放远景 B 点发出的光线创建动画
        self.play(Create(ray3_B_to_top), Create(ray4_B_to_bot))
        # 播放远景 z1, z2 点及标签动画
        self.play(FadeIn(dot_z1), FadeIn(dot_z2), FadeIn(label_z1), FadeIn(label_z2))
        
        # 创建远景物高 z 的斜向尺寸标注
        dim_z = self.create_slanted_dimension(point_z1, point_z2, "z", direction=UL, offset=0.9, color=WHITE)
        # 播放远景尺寸标注创建动画
        self.play(Create(dim_z))
        
        # 创建远景关于 z1, z2 的说明文字
        text_part2 = Text("B点发出的光线，在对焦平面处交于点z1、点z2，在对焦平面处形成物高 z", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景说明文字淡入
        self.play(FadeIn(text_part2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景说明文字淡出
        self.play(FadeOut(text_part2))

        # 计算远景主光线 1 的斜率
        slope_z1_center = (0 - y_z1) / (x_pupil - x_focus)
        # 计算远景主光线 1 在像面上的交点 y 坐标
        y_z1_prime = slope_z1_center * (x_image - x_pupil)
        # 计算远景像面交点 z'1 的坐标
        point_z1_prime = np.array([x_image, y_z1_prime, 0])
        
        # 计算远景主光线 2 的斜率
        slope_z2_center = (0 - y_z2) / (x_pupil - x_focus)
        # 计算远景主光线 2 在像面上的交点 y 坐标
        y_z2_prime = slope_z2_center * (x_image - x_pupil)
        # 计算远景像面交点 z'2 的坐标
        point_z2_prime = np.array([x_image, y_z2_prime, 0])
        
        # 创建远景主光线 1（橙色虚线）
        principal_ray1 = DashedLine(point_z1, point_z1_prime, color=ORANGE, stroke_width=2)
        # 创建远景主光线 2（橙色虚线）
        principal_ray2 = DashedLine(point_z2, point_z2_prime, color=ORANGE, stroke_width=2)
        
        # 创建从远景入瞳上边缘到像面 z'1 的出射光线
        ray3_out = self.create_ray_with_mid_arrow(point_a_top, point_z1_prime, GREEN_B, is_dashed=True)
        # 创建从远景入瞳下边缘到像面 z'2 的出射光线
        ray4_out = self.create_ray_with_mid_arrow(point_a_bot, point_z2_prime, GREEN_B, is_dashed=True)
        
        # 创建远景 z'1 点圆点
        dot_z1_prime = Dot(point_z1_prime, color=GREEN_B, radius=0.05)
        # 创建远景 z'2 点圆点
        dot_z2_prime = Dot(point_z2_prime, color=GREEN_B, radius=0.05)
        # 创建远景 z'1 点标签文字
        label_z1_prime = MathTex("z'_1", font_size=30, color=WHITE).next_to(dot_z1_prime, DOWN, buff=0.15).shift(RIGHT*0.2)
        # 创建远景 z'2 点标签文字
        label_z2_prime = MathTex("z'_2", font_size=30, color=WHITE).next_to(dot_z2_prime, UP, buff=0.15).shift(RIGHT*0.2)
        
        # 播放远景主光线创建动画
        self.play(Create(principal_ray1), Create(principal_ray2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景 z'1, z'2 点及标签动画
        self.play(FadeIn(dot_z1_prime), FadeIn(dot_z2_prime), FadeIn(label_z1_prime), FadeIn(label_z2_prime))
        # 等待 2 秒
        self.wait(2)
        # 播放远景出射光线创建动画
        self.play(Create(ray3_out), Create(ray4_out))
       
        # 创建远景第一段说明文字
        text_part3_1 = Text("z1点、z2点发出的经过入瞳中心的两条主光线，分别交于像面z'1、z'2两点", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=1.0)
        # 创建远景第二段说明文字
        text_part3_2 = Text("z'1、z'2两点之间的距离即为像高 z'", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景说明文字淡入
        self.play(FadeIn(text_part3_1), FadeIn(text_part3_2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景说明文字淡出
        self.play(FadeOut(text_part3_1), FadeOut(text_part3_2))

        # 创建远景像高 z' 的斜向尺寸标注
        dim_z_prime = self.create_slanted_dimension(point_z1_prime, point_z2_prime, "z'", direction=DR, offset=0.9, color=WHITE)
        # 播放远景尺寸标注创建动画
        self.play(Create(dim_z_prime))
        
        # 创建远景上光线说明文字 1
        text_part4_1 = Text("通过主光线确定像高z'，B点发出的上光线", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=1.0)
        # 创建远景上光线说明文字 2
        text_part4_2 = Text("经过z1点后入射到入瞳上边缘，出射后经过像面上的z'1点", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景上光线说明文字淡入
        self.play(FadeIn(text_part4_1), FadeIn(text_part4_2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景上光线说明文字淡出
        self.play(FadeOut(text_part4_1), FadeOut(text_part4_2))

        # 创建远景下光线说明文字 1
        text_part5_1 = Text("通过主光线确定像高z'，B点发出的下光线，", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=1.0)
        # 创建远景下光线说明文字 2
        text_part5_2 = Text("经过z1点后入射到入瞳下边缘，出射后经过像面上的z'2点", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景下光线说明文字淡入
        self.play(FadeIn(text_part5_1), FadeIn(text_part5_2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景下光线说明文字淡出
        self.play(FadeOut(text_part5_1), FadeOut(text_part5_2))

        # 创建远景入瞳上边缘标签文字
        label_a_top = MathTex("a_{1}", font_size=30, color=WHITE).next_to(point_a_top, RIGHT, buff=0.18)
        # 创建远景入瞳下边缘标签文字
        label_a_bot = MathTex("a_{2}", font_size=30, color=WHITE).next_to(point_a_bot, RIGHT, buff=0.18)
        # 播放远景边缘点标签淡入动画
        self.play(FadeIn(label_a_top), FadeIn(label_a_bot))
        
        # 创建远景高亮小三角形
        triangle_small = Polygon(point_B, point_z1, point_z2, color=YELLOW, fill_opacity=0.4, stroke_width=0)
        # 创建远景高亮大三角形
        triangle_large = Polygon(point_B, point_a_top, point_a_bot, color=PINK, fill_opacity=0.2, stroke_width=0.5)
        
        # 先播放远景小三角形高亮动画
        self.play(FadeIn(triangle_small))
        # 等待 3 秒
        self.wait(3)
        # 再播放远景大三角形高亮动画
        self.play(FadeIn(triangle_large))
        
        # 创建远景推导公式容器组
        derivation_group = VGroup()
        # 创建远景推导说明文字
        text_similar = Text("由 △BZ1Z2 相似于 △Ba1a2得：", font="SimHei", font_size=20, color=WHITE)
        # 将远景说明文字添加到推导组
        derivation_group.add(text_similar)
        # 创建远景大括号
        brace = MathTex(r"\left\{", font_size=100, color=WHITE)
        # 创建远景公式 1
        eq1 = MathTex(r"\frac{z}{\Delta_1} = \frac{2a}{l + \Delta_1}", font_size=36, color=WHITE)
        # 创建远景公式 2
        eq2 = MathTex(r"\Delta_1 = \frac{l z}{2a - z}", font_size=36, color=WHITE)
        # 创建远景公式 3
        eq3 = MathTex(r"\beta = \frac{z'}{z}  , \quad z' = D \varepsilon", font_size=36, color=WHITE)
        # 创建远景公式 4
        eq4 = MathTex(r"\Delta_1 = \frac{D \varepsilon l}{2a \beta - D \varepsilon}", font_size=40, color=WHITE)
        
        # 将远景公式纵向排列
        eq_group = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # 将远景大括号和公式组横向排列
        brace_and_eq = VGroup(brace, eq_group).arrange(RIGHT, buff=0.15)
        # 将远景括号和公式块添加到推导组
        derivation_group.add(brace_and_eq)
        # 将远景说明文字和括号公式块纵向排列
        derivation_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # 远景推导组缩放并移动到屏幕右侧
        derivation_group.scale(1.0).move_to(np.array([3.8, 0.5, 0]))
        
        # 播放远景说明文字淡入动画
        self.play(FadeIn(text_similar))
        # 等待 2 秒
        self.wait(2)
        # 播放远景大括号和公式 1 动画
        self.play(FadeIn(brace), Write(eq1))
        # 等待 2 秒
        self.wait(2)
        # 播放远景公式 2 动画
        self.play(Write(eq2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景公式 3 动画
        self.play(Write(eq3))
        # 等待 2 秒
        self.wait(2)
        # 播放远景公式 4 动画
        self.play(Write(eq4))
        
        # 创建远景参数说明文字 1
        text_part6_1 = Text("公式中，D为人眼明视距离，ε为人眼极限分辨角，二者均为常数", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=1.0)
        # 创建远景参数说明文字 2
        text_part6_2 = Text("因此，远景深度 Δ1 仅与对焦距离 l、入瞳口径 2a、物像放大倍率 β 有关", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5) 
        # 播放远景参数说明文字淡入
        self.play(FadeIn(text_part6_1), FadeIn(text_part6_2))
        # 等待 2 秒
        self.wait(2)
        # 播放远景参数说明文字淡出
        self.play(FadeOut(text_part6_1), FadeOut(text_part6_2))

        # 创建远景推导完成文字
        text_final = Text("远景深度 Δ1 公式推导完成", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放远景推导完成文字淡入
        self.play(FadeIn(text_final))
        # 等待 4 秒
        self.wait(4)
        
        # 清空屏幕，准备进入近景演示
        self.play(FadeOut(Group(*self.mobjects)))

        # =====================================================================
        # ==================== 近景深度演示（第二部分） =======================
        # =====================================================================
        
        # 【需求修改】重新定义近景物距 l，改为 3.25
        l_val_near = 3.25
        # 设定近景深度 delta（保持不变）
        delta_val_near = 1.0
        # 设定整体右移量（保持不变）
        shift_x_near = 1.5
        
        # 重新计算近景对焦平面 X 坐标
        x_focus_near = -l_val_near - shift_x_near
        # 重新计算近景平面 X 坐标（在焦平面右侧）
        x_near = x_focus_near + delta_val_near
        # 重新计算近景入瞳面 X 坐标（入瞳位置不变）
        x_pupil_near = -shift_x_near
        # 重新计算近景像面 X 坐标（像面位置不变）
        x_image_near = 2.0 - shift_x_near

        # 【近景标题】创建近景标题文字
        title_near = Text("二、近景深度计算", font="SimHei", font_size=72, color=WHITE)
        # 将近景标题移动到屏幕正中央
        title_near.move_to(ORIGIN)
        # 播放近景标题淡入动画
        self.play(FadeIn(title_near))
        # 停留 1.5 秒供观众看清
        self.wait(1.5)
        # 播放近景标题淡出动画
        self.play(FadeOut(title_near))
        
        # 重新创建近景光轴
        optical_axis_near = Line(start=LEFT * 7.0, end=RIGHT * 1.2, color=WHITE)
        # 重新创建近景对焦平面
        focus_plane_near = Line(start=np.array([x_focus_near, -2.2, 0]), end=np.array([x_focus_near, 2.2, 0]), color=GREEN)
        # 重新创建近景入瞳面
        pupil_line_near = Line(start=np.array([x_pupil_near, -a_val, 0]), end=np.array([x_pupil_near, a_val, 0]), color=YELLOW)
        # 重新创建近景像面
        image_plane_near = Line(start=np.array([x_image_near, -1.1, 0]), end=np.array([x_image_near, 1.1, 0]), color=BLUE)
        
        # 重新创建近景光轴标签
        label_axis_near = Text("光轴", font="SimHei", font_size=24).move_to(np.array([-6.5, -0.3, 0]))
        # 重新创建近景入瞳标签
        label_pupil_near = Text("入瞳", font="SimHei", font_size=24, color=YELLOW).next_to(pupil_line_near, UP, buff=0.3)
        # 重新创建近景对焦平面标签
        label_focus_near = Text("对焦平面", font="SimHei", font_size=24, color=GREEN).next_to(focus_plane_near, UP, buff=0.1)
        # 重新创建近景像面标签
        label_image_near = Text("像面(探测器)", font="SimHei", font_size=22, color=BLUE).next_to(image_plane_near, UP, buff=0.1)
        
        # 播放近景基础线段创建动画
        self.play(Create(optical_axis_near), Create(focus_plane_near), Create(pupil_line_near), Create(image_plane_near))
        # 播放近景基础标签淡入动画
        self.play(FadeIn(label_axis_near), FadeIn(label_pupil_near), FadeIn(label_focus_near), FadeIn(label_image_near))
        
        # 创建近景平面虚线
        near_plane = DashedLine(start=np.array([x_near, -1.6, 0]), end=np.array([x_near, 1.6, 0]), color=PURPLE)
        # 创建近景平面标签
        label_near = Text("近景平面", font="SimHei", font_size=20, color=PURPLE).next_to(near_plane, UP, buff=0.1)
        # 播放近景平面创建动画
        self.play(Create(near_plane), FadeIn(label_near))
        
        # 创建近景物距 l 标注
        dim_l_near = self.create_vertical_dimension(np.array([x_focus_near, 0, 0]), np.array([x_pupil_near, 0, 0]), "l", offset=2.3, color=WHITE)  
        # 创建近景深度 Delta_2 标注
        dim_delta_near = self.create_vertical_dimension(np.array([x_focus_near, 0, 0]), np.array([x_near, 0, 0]), r"\Delta_2", offset=1.6, color=WHITE)
        # 播放近景标注创建动画
        self.play(Create(dim_l_near), Create(dim_delta_near))
        # 等待 2 秒
        self.wait(2)

        # 重新计算近景 A 点坐标
        point_A_near = np.array([x_focus_near, 0, 0])
        # 重新计算近景入瞳上边缘点坐标
        point_a_top_near = np.array([x_pupil_near, a_val, 0])
        # 重新计算近景入瞳下边缘点坐标
        point_a_bot_near = np.array([x_pupil_near, -a_val, 0])
        # 重新计算近景像面中心点坐标
        point_image_center_near = np.array([x_image_near, 0, 0])

        # 创建近景演示的 A 点圆点
        dot_A_near = Dot(point_A_near, color=RED_E, radius=0.05)
        # 创建近景演示的 A 点标签
        label_A_near = MathTex("A", font_size=24, color=RED_E).next_to(dot_A_near, UP, buff=0.005).shift(LEFT*0.2)
        # 播放近景 A 点及标签
        self.play(FadeIn(dot_A_near), FadeIn(label_A_near))
        
        # 创建近景 A 到入瞳上边缘的光线
        ray1_A_to_top_near = self.create_ray_with_mid_arrow(point_A_near, point_a_top_near, BLUE_B)
        # 创建近景 A 到入瞳下边缘的光线
        ray2_A_to_bot_near = self.create_ray_with_mid_arrow(point_A_near, point_a_bot_near, BLUE_B)
        # 播放近景发散光线
        self.play(Create(ray1_A_to_top_near), Create(ray2_A_to_bot_near))
        # 等待 0.5 秒
        self.wait(0.5)
        
        # 创建近景入瞳到像面中心的光线
        ray1_top_to_img_near = self.create_ray_with_mid_arrow(point_a_top_near, point_image_center_near, BLUE_B)
        # 创建近景入瞳到像面中心的光线
        ray2_bot_to_img_near = self.create_ray_with_mid_arrow(point_a_bot_near, point_image_center_near, BLUE_B)
        # 播放近景汇聚光线
        self.play(Create(ray1_top_to_img_near), Create(ray2_bot_to_img_near))
        # 等待 1 秒
        self.wait(1)

        # 【需求修改】近景平面上的点命名为 B，不用 B'
        point_B_near = np.array([x_near, 0, 0])
        # 创建 B 点圆点
        dot_B_near = Dot(point_B_near, color=YELLOW)
        # 创建 B 点标签文字（显示为 B）
        label_B_near = MathTex("B", font_size=24, color=YELLOW).next_to(dot_B_near, DOWN, buff=0.005).shift(LEFT*0.2)
        # 播放 B 点及标签
        self.play(FadeIn(dot_B_near), FadeIn(label_B_near))
        
        # 计算从 B 到近景入瞳上边缘的斜率
        slope_3_near = (a_val - 0) / (x_pupil_near - x_near)
        # 计算光线反向延长后与对焦平面的交点 y 坐标
        y_z1_near = slope_3_near * (x_focus_near - x_near)
        # 计算交点 z1 的坐标
        point_z1_near = np.array([x_focus_near, y_z1_near, 0])
        
        # 计算从 B 到近景入瞳下边缘的斜率
        slope_4_near = (-a_val - 0) / (x_pupil_near - x_near)
        # 计算光线反向延长后与对焦平面的交点 y 坐标
        y_z2_near = slope_4_near * (x_focus_near - x_near)
        # 计算交点 z2 的坐标
        point_z2_near = np.array([x_focus_near, y_z2_near, 0])
        
        # 创建 B 到近景入瞳上边缘的光线（向右的虚线）
        ray3_B_to_top_near = self.create_ray_with_mid_arrow(point_B_near, point_a_top_near, GREEN_B, is_dashed=True)
        # 创建 B 到近景入瞳下边缘的光线（向右的虚线）
        ray4_B_to_bot_near = self.create_ray_with_mid_arrow(point_B_near, point_a_bot_near, GREEN_B, is_dashed=True)
        
        # 创建 B 到近景 z1 的反向延长线（向左的虚线）
        ray3_reverse_near = self.create_ray_with_mid_arrow(point_B_near, point_z1_near, GREEN_B, is_dashed=True)
        # 创建 B 到近景 z2 的反向延长线（向左的虚线）
        ray4_reverse_near = self.create_ray_with_mid_arrow(point_B_near, point_z2_near, GREEN_B, is_dashed=True)
        
        # 创建近景的 z1 点圆点
        dot_z1_near = Dot(point_z1_near, color=WHITE, radius=0.06)
        # 创建近景的 z2 点圆点
        dot_z2_near = Dot(point_z2_near, color=WHITE, radius=0.06)
        # 创建近景的 z1 点标签
        label_z1_near = MathTex("z_1", font_size=30, color=WHITE).next_to(dot_z1_near, DOWN, buff=0.18).shift(RIGHT*0.3)
        # 创建近景的 z2 点标签
        label_z2_near = MathTex("z_2", font_size=30, color=WHITE).next_to(dot_z2_near, UP, buff=0.18).shift(RIGHT*0.3)
        
        # 播放向右的光线
        self.play(Create(ray3_B_to_top_near), Create(ray4_B_to_bot_near))
        # 播放向左的反向延长线
        self.play(Create(ray3_reverse_near), Create(ray4_reverse_near))
        # 播放交点及标签
        self.play(FadeIn(dot_z1_near), FadeIn(dot_z2_near), FadeIn(label_z1_near), FadeIn(label_z2_near))
        
        # 创建近景物高 z 的标注
        dim_z_near = self.create_slanted_dimension(point_z1_near, point_z2_near, "z", direction=UL, offset=1.1, color=WHITE)
        # 播放物高标注
        self.play(Create(dim_z_near))
        
        # 创建近景物高说明文字
        text_part2_near = Text("B发出的光线向右入射，其反向延长线与对焦平面交于z1、z2，形成物高z", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放说明文字
        self.play(FadeIn(text_part2_near))
        # 等待 2 秒
        self.wait(2)
        # 播放说明文字淡出
        self.play(FadeOut(text_part2_near))

        # 计算近景主光线 1 的斜率
        slope_z1_center_near = (0 - y_z1_near) / (x_pupil_near - x_focus_near)
        # 计算主光线 1 与像面交点 z'1 的 y 坐标
        y_z1_prime_near = slope_z1_center_near * (x_image_near - x_pupil_near)
        # 计算 z'1 点坐标
        point_z1_prime_near = np.array([x_image_near, y_z1_prime_near, 0])
        
        # 计算近景主光线 2 的斜率
        slope_z2_center_near = (0 - y_z2_near) / (x_pupil_near - x_focus_near)
        # 计算主光线 2 与像面交点 z'2 的 y 坐标
        y_z2_prime_near = slope_z2_center_near * (x_image_near - x_pupil_near)
        # 计算 z'2 点坐标
        point_z2_prime_near = np.array([x_image_near, y_z2_prime_near, 0])
        
        # 创建近景主光线 1
        principal_ray1_near = DashedLine(point_z1_near, point_z1_prime_near, color=ORANGE, stroke_width=2)
        # 创建近景主光线 2
        principal_ray2_near = DashedLine(point_z2_near, point_z2_prime_near, color=ORANGE, stroke_width=2)
        
        # 创建近景出射光线 1
        ray3_out_near = self.create_ray_with_mid_arrow(point_a_top_near, point_z1_prime_near, GREEN_B, is_dashed=True)
        # 创建近景出射光线 2
        ray4_out_near = self.create_ray_with_mid_arrow(point_a_bot_near, point_z2_prime_near, GREEN_B, is_dashed=True)
        
        # 创建近景 z'1 点圆点
        dot_z1_prime_near = Dot(point_z1_prime_near, color=GREEN_B, radius=0.05)
        # 创建近景 z'2 点圆点
        dot_z2_prime_near = Dot(point_z2_prime_near, color=GREEN_B, radius=0.05)
        # 创建近景 z'1 标签
        label_z1_prime_near = MathTex("z'_1", font_size=22, color=WHITE).next_to(dot_z1_prime_near, UP, buff=0.005).shift(RIGHT*0.2)
        # 创建近景 z'2 标签
        label_z2_prime_near = MathTex("z'_2", font_size=22, color=WHITE).next_to(dot_z2_prime_near, DOWN, buff=0.005).shift(RIGHT*0.2)
        
        # 播放近景主光线
        self.play(Create(principal_ray1_near), Create(principal_ray2_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景 z'1, z'2 点及标签
        self.play(FadeIn(dot_z1_prime_near), FadeIn(dot_z2_prime_near), FadeIn(label_z1_prime_near), FadeIn(label_z2_prime_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景出射光线
        self.play(Create(ray3_out_near), Create(ray4_out_near))
        
        # 创建近景像高说明文字
        text_part3_near = Text("主光线交于像面确定像高 z'，边缘光线出射后分别经过 z'1、z'2", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放说明文字
        self.play(FadeIn(text_part3_near))
        # 等待 2 秒
        self.wait(2)
        # 播放说明文字淡出
        self.play(FadeOut(text_part3_near))

        # 创建近景像高 z' 的标注
        dim_z_prime_near = self.create_slanted_dimension(point_z1_prime_near, point_z2_prime_near, "z'", direction=DR, offset=0.9, color=WHITE)
        # 播放像高标注
        self.play(Create(dim_z_prime_near))
        
        # 创建近景入瞳上边缘标签
        label_a_top2 = MathTex("a_{1}", font_size=30, color=WHITE).next_to(point_a_top_near, RIGHT, buff=0.18)
        # 创建近景入瞳下边缘标签
        label_a_bot2 = MathTex("a_{2}", font_size=30, color=WHITE).next_to(point_a_bot_near, RIGHT, buff=0.18)
        # 播放边缘标签淡入
        self.play(FadeIn(label_a_top2), FadeIn(label_a_bot2))
        
        # 创建近景高亮小三角形
        triangle_small_near = Polygon(point_B_near, point_z1_near, point_z2_near, color=YELLOW, fill_opacity=0.4, stroke_width=0)
        # 创建近景高亮大三角形
        triangle_large_near = Polygon(point_B_near, point_a_top_near, point_a_bot_near, color=PINK, fill_opacity=0.2, stroke_width=0.5)
        
        # 播放小三角形高亮
        self.play(FadeIn(triangle_small_near))
        # 等待 2 秒
        self.wait(2)
        # 播放大三角形高亮
        self.play(FadeIn(triangle_large_near))
        
        # 创建近景公式推导组
        derivation_group_near = VGroup()
        # 【需求修改】近景推导说明文字，去掉 B 后面的 ' 符号
        text_similar_near = Text("由 △BZ1Z2 相似于 △Ba1a2得：", font="SimHei", font_size=20, color=WHITE)
        # 添加说明文字到推导组
        derivation_group_near.add(text_similar_near)
        # 创建近景大括号
        brace_near = MathTex(r"\left\{", font_size=100, color=WHITE)
        
        # 创建近景公式 1（分母为减号）
        eq1_near = MathTex(r"\frac{z}{\Delta_2} = \frac{2a}{l - \Delta_2}", font_size=36, color=WHITE)
        # 创建近景公式 2（分母为加号）
        eq2_near = MathTex(r"\Delta_2 = \frac{l z}{2a + z}", font_size=36, color=WHITE)
        # 创建近景公式 3
        eq3_near = MathTex(r"\beta = \frac{z'}{z}  , \quad z' = D \varepsilon", font_size=36, color=WHITE)
        # 创建近景公式 4（分母为加号）
        eq4_near = MathTex(r"\Delta_2 = \frac{D \varepsilon l}{2a \beta + D \varepsilon}", font_size=40, color=WHITE)
        
        # 纵向排列近景公式
        eq_group_near = VGroup(eq1_near, eq2_near, eq3_near, eq4_near).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # 横向排列近景大括号和公式组
        brace_and_eq_near = VGroup(brace_near, eq_group_near).arrange(RIGHT, buff=0.15)
        # 将括号和公式块添加到推导组
        derivation_group_near.add(brace_and_eq_near)
        # 排列推导组内的文字和公式块
        derivation_group_near.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # 缩放并移动到右侧固定位置
        derivation_group_near.scale(1.0).move_to(np.array([3.8, 0.5, 0]))
        
        # 播放近景推导说明文字
        self.play(FadeIn(text_similar_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景大括号和公式 1
        self.play(FadeIn(brace_near), Write(eq1_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景公式 2
        self.play(Write(eq2_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景公式 3
        self.play(Write(eq3_near))
        # 等待 1 秒
        self.wait(1)
        # 播放近景公式 4
        self.play(Write(eq4_near))
        
        # 创建近景推导完成文字
        text_final_near = Text("近景深度 Δ2 公式推导完成", font="SimHei", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        # 播放近景推导完成文字
        self.play(FadeIn(text_final_near))
        # 等待 4 秒
        self.wait(4)
        
        # 清空屏幕所有元素，准备播放片尾
        self.play(FadeOut(Group(*self.mobjects)))

        # =====================================================================
        # ==================== 片尾跳动字幕 ===================================
        # =====================================================================
        
        # 定义片尾字符串
        text_str = "视频由@玻璃窗-Simon制作"
        # 利用列表推导式，将每个字符创建为独立的 Text 对象，放入 VGroup 中
        text_chars = VGroup(*[Text(char, font="SimHei", font_size=40, color=WHITE) for char in text_str])
        # 将单个字符横向排列（设置微小间距），然后将整体移动到画面正中央
        text_chars.arrange(RIGHT, buff=0.05).move_to(ORIGIN)

        # 播放“依次跳动出现”的动画
        self.play(
            # 使用 LaggedStart 实现延迟依次播放
            LaggedStart(
                # 遍历每一个字符，实现从下方弹起并淡入的效果
                *[FadeIn(char, shift=UP * 0.5) for char in text_chars],
                # 延迟比率，控制字跳出的速度
                lag_ratio=0.15
            )
        )

        # 等待 3 秒，供观众看清文字
        self.wait(3)

        # 淡出所有元素，结束整个视频
        self.play(FadeOut(Group(*self.mobjects)))