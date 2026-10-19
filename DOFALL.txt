# 导入 manim 库中的所有类，如几何图形、文字、动画等
from manim import *
# 导入 numpy 库，用于进行高精度的数学和数组计算
import numpy as np

# 修改全局渲染背景颜色为深灰色，突出亮色线条
config.background_color = "#1C1C1C"

# 定义动态景深演示场景类，继承自 Manim 的基础场景类
class DynamicDOFScene(Scene):
    # 定义构建方法，这是所有动画渲染的逻辑入口
    def construct(self):
        # ==================== 1. 物理参数与坐标系设定 ====================
        # 设定入瞳的半径（透镜的半口径）
        a = 0.5
        # 设定当前对焦平面的物距
        u0 = 3.0
        # 设定像距（像面到入瞳的距离）
        v = 1.5
        # 根据薄透镜成像公式，计算透镜焦距的倒数 (1/f = 1/u + 1/v)
        f_inv = 1 / u0 + 1 / v
        
        # 计算对焦平面的 x 坐标（在光轴左侧为负）
        x_focus = -u0
        # 计算远景平面的 x 坐标（设定物距为 6）
        x_far = -6.0
        # 计算近景平面的 x 坐标（设定物距为 2）
        x_near = -2.0
        # 设定入瞳面的 x 坐标为 0，作为光轴坐标原点
        x_pupil = 0.0
        # 设定像面的 x 坐标
        x_image = v
        
        # 设定人眼明视距离 D
        D = 2.0
        # 计算人眼中心的 x 坐标（在像面右侧距离 D 处）
        x_eye = x_image + D
        # 设定人眼外轮廓的半径
        R_eye = 0.3

        # 设定极限分辨角对应的像面半高度
        y_eps = 0.125
        # 计算动态弥散圆的缩放系数，确保在远景/近景时刚好充满人眼
        blur_scale = R_eye / y_eps

        # ==================== 2. 顶部文字说明 ====================
        # 创建第一行文字说明，解释景深与观察条件
        text_line1 = Text("在景深（Δ1+Δ2）范围内，人眼在明视距离D处观察像高z'", font="SimHei", font_size=20, color=WHITE)
        # 创建第二行文字说明，解释为什么景深内景物是清晰的
        text_line2 = Text("像高z'对人眼的张角θ始终小于人眼极限分辨角ε，故景深范围内的景物对人眼来说都是清晰的", font="SimHei", font_size=20, color=WHITE)
        # 将两行文字组合成一个组
        text_group = VGroup(text_line1, text_line2)
        # 将两行文字纵向排列，左对齐，并放置在画面正上方
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.3)

        # ==================== 3. 创建静态基础元素 ====================
        # 创建横跨屏幕的光轴线段
        optical_axis = Line(start=LEFT * 8, end=RIGHT * 7, color=WHITE)
        # 创建光轴文字标签，放置在最左侧下方
        label_axis = Text("光轴", font="SimHei", font_size=20).next_to(optical_axis, DOWN, buff=0.1).shift(LEFT * 6)
        
        # 创建远景平面（紫色虚线）
        far_plane = DashedLine(start=np.array([x_far, -1.5, 0]), end=np.array([x_far, 1.5, 0]), color=PURPLE)
        # 创建远景平面文字标签
        label_far = Text("远景平面", font="SimHei", font_size=15, color=PURPLE).next_to(far_plane, UP, buff=0.2)
        
        # 创建对焦平面（绿色实线）
        focus_plane = Line(start=np.array([x_focus, -1.5, 0]), end=np.array([x_focus, 1.5, 0]), color=GREEN)
        # 创建对焦平面文字标签
        label_focus = Text("对焦平面", font="SimHei", font_size=18, color=GREEN).next_to(focus_plane, UP, buff=0.25)
        
        # 创建近景平面（紫色虚线）
        near_plane = DashedLine(start=np.array([x_near, -1.5, 0]), end=np.array([x_near, 1.5, 0]), color=PURPLE)
        # 创建近景平面文字标签
        label_near = Text("近景平面", font="SimHei", font_size=15, color=PURPLE).next_to(near_plane, UP, buff=0.1)
        
        # 创建入瞳面（黄色粗线）
        pupil_line = Line(start=np.array([x_pupil, -a, 0]), end=np.array([x_pupil, a, 0]), color=YELLOW, stroke_width=4)
        # 创建入瞳面文字标签
        label_pupil = Text("入瞳", font="SimHei", font_size=20, color=YELLOW).next_to(pupil_line, UP, buff=0.3)
        
        # 在入瞳中心画一个白色小点，强调中心位置
        pupil_center_dot = Dot(ORIGIN, color=WHITE, radius=0.05)
        
        # 创建像面（蓝色实线）
        image_plane = Line(start=np.array([x_image, -1.5, 0]), end=np.array([x_image, 1.5, 0]), color=BLUE)
        # 创建像面文字标签
        label_image = Text("像面", font="SimHei", font_size=18, color=BLUE).next_to(image_plane, UP, buff=0.2)
        
        # 创建人眼外轮廓（白色圆圈）
        eye_outer = Circle(radius=R_eye, color=WHITE).move_to(np.array([x_eye, 0, 0]))
        # 创建人眼瞳孔（白色圆点，偏左代表向左看）
        eye_pupil = Dot(point=np.array([x_eye - 0.1, 0, 0]), radius=0.08, color=WHITE)
        # 创建人眼文字标签，放在眼睛正下方
        label_eye = Text("人眼", font="SimHei", font_size=18, color=WHITE).next_to(eye_outer, DR, buff=0.3)

        # ==================== 4. 工程制图尺寸标注（静态） ====================
        # 定义通用的水平尺寸标注辅助函数
        def create_engineering_dimension(x1, x2, y_pos, text, start_y=-1.5):
            # 计算尺寸线的左侧端点
            p1 = np.array([x1, y_pos, 0])
            # 计算尺寸线的右侧端点
            p2 = np.array([x2, y_pos, 0])
            # 绘制左侧从原平面延伸下来的细引线
            ext1 = Line(np.array([x1, start_y, 0]), p1, color=WHITE, stroke_width=1)
            # 绘制右侧从原平面延伸下来的细引线
            ext2 = Line(np.array([x2, start_y, 0]), p2, color=WHITE, stroke_width=1)
            # 绘制主尺寸线
            dim_line = Line(p1, p2, color=WHITE, stroke_width=1.5)
            # 绘制左侧朝内的箭头
            arr1 = Arrow(p1 + RIGHT*0.3, p1, buff=0, color=WHITE, tip_length=0.15)
            # 绘制右侧朝内的箭头
            arr2 = Arrow(p2 + LEFT*0.3, p2, buff=0, color=WHITE, tip_length=0.15)
            
            # 判断传入的文字是否为“明视距离D”
            if text == "明视距离D":
                # 中英文混合使用 Text 类创建标签
                lbl = Text(text, font="SimHei", font_size=20, color=WHITE).next_to(dim_line, DOWN, buff=0.1)
            # 如果是其他数学符号
            else:
                # 纯数学符号使用 MathTex 类创建标签
                lbl = MathTex(text, font_size=28, color=WHITE).next_to(dim_line, DOWN, buff=0.1)
            # 返回包含所有元素的尺寸标注组
            return VGroup(ext1, ext2, dim_line, arr1, arr2, lbl)

        # 创建远景深度 Δ1 标注：从远景平面到对焦平面
        dim_delta1 = create_engineering_dimension(x_far, x_focus, -1.9, r"\Delta_1")
        # 创建近景深度 Δ2 标注：从对焦平面到近景平面
        dim_delta2 = create_engineering_dimension(x_focus, x_near, -1.9, r"\Delta_2")
        # 创建对焦距离 l 标注：从对焦平面到入瞳面
        dim_l = create_engineering_dimension(x_focus, x_pupil, -2.6, "l")
        # 创建明视距离 D 标注：从像面到人眼中心
        dim_D = create_engineering_dimension(x_image, x_eye, -2.5, "明视距离D", start_y=-R_eye)

        # ==================== 5. 极限分辨角辅助线（静态） ====================
        # 计算极限像高在像面上的上端点
        p_eps_top = np.array([x_image, y_eps, 0])
        # 计算极限像高在像面上的下端点
        p_eps_bot = np.array([x_image, -y_eps, 0])
        # 获取人眼中心坐标
        eye_center = np.array([x_eye, 0, 0])
        
        # 绘制从极限像高上端点指向人眼的灰色实线
        eps_line_top = Line(p_eps_top, eye_center, color=WHITE, stroke_width=2.0)
        # 绘制从极限像高下端点指向人眼的灰色实线
        eps_line_bot = Line(p_eps_bot, eye_center, color=WHITE, stroke_width=2.0)

        # ==================== 6. 对焦平面的静态光路 ====================
        # 计算对焦平面的中心点 A 的坐标
        p_A = np.array([x_focus, 0, 0])
        # 绘制从 A 点发散到入瞳上边缘的入射光线
        static_ray_in_top = Line(p_A, np.array([x_pupil, a, 0]), color=BLUE_B, stroke_width=1.5)
        # 绘制从 A 点发散到入瞳下边缘的入射光线
        static_ray_in_bot = Line(p_A, np.array([x_pupil, -a, 0]), color=BLUE_B, stroke_width=1.5)
        # 绘制从入瞳上边缘汇聚到像面中心的出射光线
        static_ray_out_top = Line(np.array([x_pupil, a, 0]), np.array([x_image, 0, 0]), color=BLUE_B, stroke_width=1.5)
        # 绘制从入瞳下边缘汇聚到像面中心的出射光线
        static_ray_out_bot = Line(np.array([x_pupil, -a, 0]), np.array([x_image, 0, 0]), color=BLUE_B, stroke_width=1.5)

        # ==================== 7. 播放静态元素的创建动画 ====================
        # 播放顶部两行文字说明的淡入动画
        self.play(FadeIn(text_group))
        # 播放基础平面（光轴、各平面、入瞳、像面）的创建动画
        self.play(Create(optical_axis), Create(far_plane), Create(focus_plane), Create(near_plane), Create(pupil_line), Create(image_plane))
        # 播放所有文字标签和人眼图标的淡入动画
        self.play(FadeIn(label_axis), FadeIn(label_far), FadeIn(label_focus), FadeIn(label_near), FadeIn(label_pupil), FadeIn(label_image))
        # 播放人眼轮廓、瞳孔和标签的创建动画
        self.play(Create(eye_outer), FadeIn(eye_pupil), FadeIn(label_eye))
        
        # 播放底部所有工程尺寸标注的创建动画
        self.play(Create(dim_delta1), Create(dim_delta2), Create(dim_l), Create(dim_D), run_time=2)
        
        # 播放极限分辨角辅助线及入瞳中心点的创建动画
        self.play(Create(eps_line_top), Create(eps_line_bot), FadeIn(pupil_center_dot))
        
        # 物理上先播放 A 点光线的发散过程（到达入瞳）
        self.play(Create(static_ray_in_top), Create(static_ray_in_bot), run_time=1)
        # 停顿 0.5 秒，体现光线到达透镜的瞬间
        self.wait(0.5)
        # 再播放光线经过透镜折射后的汇聚过程（到达像面）
        self.play(Create(static_ray_out_top), Create(static_ray_out_bot), run_time=1)
        # 停顿 1 秒观察结果
        self.wait(1)

        # ==================== 8. 定义动态组件与工程标注辅助函数 ====================
        # 创建追踪假想平面的 X 坐标追踪器，初始值为远景平面的位置
        x_tracker = ValueTracker(x_far)
        
        # 动态绘制假想平面（黄色实线）
        plane = always_redraw(lambda: Line(np.array([x_tracker.get_value(), -1.2, 0]), np.array([x_tracker.get_value(), 1.2, 0]), color=YELLOW, stroke_width=3))
        
        # 【新增】动态绘制假想平面中心的蓝色圆点，随平面移动
        plane_center_dot = always_redraw(lambda: Dot(np.array([x_tracker.get_value(), 0, 0]), color=BLUE, radius=0.06))
        
        # 动态放置假想平面的文字标签
        label_plane = always_redraw(lambda: Text("假想平面", font="SimHei", font_size=18, color=YELLOW).next_to(plane, DOWN, buff=0.1))

        # 辅助函数：绘制动态的斜向尺寸标注
        def create_dynamic_dimension(p1, p2, text, direction, offset=0.6):
            # 如果是左上方向
            if direction == "UL":
                # 计算左上的单位方向向量
                unit_vec = np.array([-1, 1, 0]) / np.sqrt(2)
            # 如果是右下方向
            else:
                # 计算右下的单位方向向量
                unit_vec = np.array([1, -1, 0]) / np.sqrt(2)
            
            # 计算左侧延伸端点的坐标
            ext_p1 = p1 + unit_vec * offset
            # 计算右侧延伸端点的坐标
            ext_p2 = p2 + unit_vec * offset
            
            # 绘制左侧的细引线
            line_ext1 = Line(p1, ext_p1 + unit_vec * 0.1, color=WHITE, stroke_width=1)
            # 绘制右侧的细引线
            line_ext2 = Line(p2, ext_p2 + unit_vec * 0.1, color=WHITE, stroke_width=1)
            # 绘制主尺寸线
            dim_line = Line(ext_p1, ext_p2, color=WHITE, stroke_width=1.5)
            
            # 计算尺寸线的方向向量
            line_vec = ext_p2 - ext_p1
            # 计算尺寸线的单位方向向量
            line_unit = line_vec / np.linalg.norm(line_vec)
            
            # 绘制左上端朝内的箭头
            arrow1 = Arrow(ext_p1 + line_unit * 0.3, ext_p1, buff=0, color=WHITE, tip_length=0.1)
            # 绘制右下端朝内的箭头
            arrow2 = Arrow(ext_p2 - line_unit * 0.3, ext_p2, buff=0, color=WHITE, tip_length=0.1)
            
            # 计算尺寸线的中点
            mid = (ext_p1 + ext_p2) / 2
            # 计算文字的位置（向法线方向偏移一点）
            text_pos = mid + unit_vec * 0.2
            # 创建尺寸文字标签
            label = MathTex(text, font_size=22, color=WHITE).move_to(text_pos)
            
            # 返回包含所有标注元素的组
            return VGroup(line_ext1, line_ext2, dim_line, arrow1, arrow2, label)

        # 定义所有动态图元的主函数
        def get_dynamic_visuals():
            # 获取当前假想面的 x 坐标
            x_val = x_tracker.get_value()
            # 防止坐标归零导致除零错误
            if abs(x_val) < 0.05: x_val = -0.05
            
            # 计算当前物距
            u = -x_val
            # 根据高斯公式计算当前像距
            v_prime = 1 / (f_inv - 1/u)
            
            # 计算上边缘光线在像面的交点高度
            y_img_top = a * (1 - x_image / v_prime)
            # 下边缘光线高度对称
            y_img_bot = -y_img_top
            
            # 计算上边缘光线与对焦平面的交点 z1 的斜率
            slope_in = a / (0 - x_val)
            # 计算 z1 的纵坐标
            y_z1 = slope_in * (x_focus - x_val)
            # 获取 z1 坐标点
            p_z1 = np.array([x_focus, y_z1, 0])
            
            # 计算下边缘光线与对焦平面的交点 z2 的斜率
            slope_in_b = -a / (0 - x_val)
            # 计算 z2 的纵坐标
            y_z2 = slope_in_b * (x_focus - x_val)
            # 获取 z2 坐标点
            p_z2 = np.array([x_focus, y_z2, 0])
            
            # 计算主光线1在像面的交点高度
            y_z1_prime = y_z1 * x_image / (-x_focus)
            # 获取像面交点 z'1 坐标点
            p_z1_prime = np.array([x_image, y_z1_prime, 0])
            
            # 计算主光线2在像面的交点高度
            y_z2_prime = y_z2 * x_image / (-x_focus)
            # 获取像面交点 z'2 坐标点
            p_z2_prime = np.array([x_image, y_z2_prime, 0])
            
            # 绘制从 z1 指向入瞳中心的主光线第一段（虚线）
            main_ray1_p1 = DashedLine(p_z1, ORIGIN, color=ORANGE, stroke_width=2.0)
            # 绘制从入瞳中心指向像面 z'1 的主光线第二段（虚线）
            main_ray1_p2 = DashedLine(ORIGIN, p_z1_prime, color=ORANGE, stroke_width=2.0)
            # 绘制从 z2 指向入瞳中心的主光线第一段（虚线）
            main_ray2_p1 = DashedLine(p_z2, ORIGIN, color=ORANGE, stroke_width=2.0)
            # 绘制从入瞳中心指向像面 z'2 的主光线第二段（虚线）
            main_ray2_p2 = DashedLine(ORIGIN, p_z2_prime, color=ORANGE, stroke_width=2.0)
            
            # 绘制从假想面出发到入瞳上边缘的红色边缘光线
            ray1_in = Line(np.array([x_val, 0, 0]), np.array([0, a, 0]), color=RED, stroke_width=2.0)
            # 绘制从假想面出发到入瞳下边缘的红色边缘光线
            ray2_in = Line(np.array([x_val, 0, 0]), np.array([0, -a, 0]), color=RED, stroke_width=2.0)
            # 绘制从上边缘折射到像面的红色边缘光线
            ray1_out = Line(np.array([0, a, 0]), np.array([x_image, y_img_top, 0]), color=RED, stroke_width=2.0)
            # 绘制从下边缘折射到像面的红色边缘光线
            ray2_out = Line(np.array([0, -a, 0]), np.array([x_image, y_img_bot, 0]), color=RED, stroke_width=2.0)
            
            # 在对焦平面的 z1 点绘制白点
            d_z1 = Dot(p_z1, color=WHITE, radius=0.04)
            # 在对焦平面的 z2 点绘制白点
            d_z2 = Dot(p_z2, color=WHITE, radius=0.04)
            # 在像面的 z'1 点绘制黄点
            d_z1_prime = Dot(p_z1_prime, color=YELLOW, radius=0.04)
            # 在像面的 z'2 点绘制黄点
            d_z2_prime = Dot(p_z2_prime, color=YELLOW, radius=0.04)
            
            # 绘制从像面 z'1 点指向人眼的橙色实线
            eye_line_top = Line(p_z1_prime, eye_center, color=ORANGE, stroke_width=1.5)
            # 绘制从像面 z'2 点指向人眼的橙色实线
            eye_line_bot = Line(p_z2_prime, eye_center, color=ORANGE, stroke_width=1.5)
            
            # 如果物高存在（大于极小值）
            if abs(y_z1 - y_z2) > 0.05:
                # 创建对焦平面上的动态物高 z 标注（左上方向）
                dim_z = create_dynamic_dimension(p_z1, p_z2, "z", "UL", offset=0.8)
            # 如果物高太小
            else:
                # 返回空组
                dim_z = VGroup()
                
            # 如果像高存在（大于极小值）
            if abs(y_z1_prime - y_z2_prime) > 0.05:
                # 创建像面上的动态像高 z' 标注（右下方向）
                dim_z_prime = create_dynamic_dimension(p_z1_prime, p_z2_prime, "z'", "DR", offset=0.8)
            # 如果像高太小
            else:
                # 返回空组
                dim_z_prime = VGroup()
            
            # 计算人眼处动态弥散圆的半径
            r_blur = abs(y_img_top) * blur_scale
            # 绘制弥散圆的虚线轮廓
            circle_dash = Circle(radius=r_blur, color=ORANGE, stroke_width=2)
            # 设置虚线样式
            circle_dash.stroke_dash_array = [0.05, 0.05]
            # 将虚线圆移动到人眼位置
            circle_dash.move_to(eye_center)
            # 绘制弥散圆内部的半透明填充圆
            fill_circle = Circle(radius=r_blur, fill_color=ORANGE, fill_opacity=0.3, stroke_width=0)
            # 将填充圆移动到人眼位置
            fill_circle.move_to(eye_center)
            
            # 返回所有动态图元的组
            return VGroup(ray1_in, ray2_in, ray1_out, ray2_out, 
                          main_ray1_p1, main_ray2_p1, main_ray1_p2, main_ray2_p2, 
                          d_z1, d_z2, d_z1_prime, d_z2_prime, 
                          eye_line_top, eye_line_bot, 
                          circle_dash, fill_circle, 
                          dim_z, dim_z_prime)

        # 将动态图元主函数绑定到 always_redraw，实现每帧重绘
        dynamic_group = always_redraw(get_dynamic_visuals)

        # ==================== 9. 播放平移动画 ====================
        # 播放假想平面及其标签、中心蓝色点的创建动画
        self.play(Create(plane), FadeIn(label_plane), FadeIn(plane_center_dot))
        # 播放动态光路及标注的创建动画
        self.play(Create(dynamic_group))
        # 停顿 1 秒观察初始状态
        self.wait(1)

        # 动画：将假想平面平滑移动到近景平面位置
        self.play(x_tracker.animate.set_value(x_near), run_time=6, rate_func=smooth)
        # 在近景位置停顿 1 秒
        self.wait(1)
        
        # 动画：将假想平面平滑移回远景平面位置
        self.play(x_tracker.animate.set_value(x_far), run_time=6, rate_func=smooth)
        # 回到远景后停顿 2 秒
        self.wait(2)
        
        # 画面所有元素淡出，动画结束
        self.play(FadeOut(Group(*self.mobjects)))